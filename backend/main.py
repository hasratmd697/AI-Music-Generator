import base64
from typing import List
import uuid
import modal
from pydantic import BaseModel
import requests

from prompts import LYRICS_GENERATOR_PROMPT, PROMPT_GENERATOR_PROMPT

app = modal.App("music-generator")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg",)
    .pip_install_from_requirements("requirements.txt")
    .run_commands([
        "git clone https://github.com/ace-step/ACE-Step.git /tmp/ACE-Step",
        "cd /tmp/ACE-Step && pip install .",
        "pip install torchcodec"
    ])
    .env({"HF_HOME": "/.cache/huggingface"})
    .add_local_python_source("prompts")
)

model_volume = modal.Volume.from_name(
    "ace-step-models", create_if_missing=True)
hf_volume = modal.Volume.from_name("qwen-hf-cache", create_if_missing=True)

music_gen_secrets = modal.Secret.from_name("music-gen-secret")


class AudioGenerationBase(BaseModel):
    audio_duration: float = 180.0
    seed: int = -1
    guidance_scale: float = 15.0
    infer_step: int = 60
    instrumental: bool = False


class GenerateFromDescriptionRequest(AudioGenerationBase):
    full_described_song: str


class GenerateWithCustomLyricsRequest(AudioGenerationBase):
    prompt: str
    lyrics: str


class GenerateWithDescribedLyricsRequest(AudioGenerationBase):
    prompt: str
    described_lyrics: str


class GenerateMusicResponse(BaseModel):
    audio_data: str  # base64 encoded audio
    cover_image_data: str  # base64 encoded image
    categories: List[str]


@app.cls(
    image=image,
    gpu="L40S",
    volumes={"/models": model_volume, "/.cache/huggingface": hf_volume},
    secrets=[music_gen_secrets],
    scaledown_window=15
)
class MusicGenServer:
    @modal.enter()
    def load_model(self):
        from acestep.pipeline_ace_step import ACEStepPipeline
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from diffusers import AutoPipelineForText2Image
        import torch

        # Music Generation Model
        self.music_model = ACEStepPipeline(
            checkpoint_dir="/models",
            dtype="bfloat16",
            torch_compile=False,
            cpu_offload=False,
            overlapped_decode=False
        )

        # Large Language Model
        model_id = "Qwen/Qwen2-7B-Instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        self.llm_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto",
            cache_dir="/.cache/huggingface"
        )

        # Stable Diffusion Model (thumbnails)
        self.image_pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16", cache_dir="/.cache/huggingface")
        self.image_pipe.to("cuda")

    def prompt_qwen(self, question: str):
        messages = [
            {"role": "user", "content": question}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer(
            [text], return_tensors="pt").to(self.llm_model.device)

        generated_ids = self.llm_model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True)[0]

        return response

    def generate_prompt(self, description: str):
        full_prompt = PROMPT_GENERATOR_PROMPT.format(user_prompt=description)
        return self.prompt_qwen(full_prompt)

    def generate_lyrics(self, description: str):
        full_prompt = LYRICS_GENERATOR_PROMPT.format(description=description)
        return self.prompt_qwen(full_prompt)

    def generate_categories(self, description: str) -> List[str]:
        prompt = f"Based on the following music description, list 3-5 relevant genres or categories as a comma-separated list. For example: Pop, Electronic, Sad, 80s. Description: '{description}'"
        response_text = self.prompt_qwen(prompt)
        categories = [cat.strip() for cat in response_text.split(",") if cat.strip()]
        return categories

    def generate_music_with_cover(
            self,
            prompt: str,
            lyrics: str,
            instrumental: bool,
            audio_duration: float,
            infer_step: int,
            guidance_scale: float,
            seed: int,
            description_for_categorization: str
    ) -> GenerateMusicResponse:
        import io

        final_lyrics = "[instrumental]" if instrumental else lyrics
        print(f"Generated lyrics: \n{final_lyrics}")
        print(f"Prompt: \n{prompt}")

        output_dir = "/tmp/outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")

        # Generate music
        self.music_model(
            prompt=prompt,
            lyrics=final_lyrics,
            audio_duration=audio_duration,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            save_path=output_path,
            manual_seeds=str(seed)
        )

        # Read and encode audio
        with open(output_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        os.remove(output_path)

        # Generate thumbnail
        thumbnail_prompt = f"{prompt}, album cover art"
        image = self.image_pipe(
            prompt=thumbnail_prompt, num_inference_steps=2, guidance_scale=0.0).images[0]

        # Encode image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        image_b64 = base64.b64encode(img_buffer.read()).decode("utf-8")

        # Generate categories
        categories = self.generate_categories(description_for_categorization)

        return GenerateMusicResponse(
            audio_data=audio_b64,
            cover_image_data=image_b64,
            categories=categories
        )

    # @modal.fastapi_endpoint(method="POST", requires_proxy_auth=True)
    @modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
    def generate_from_description(self, request: GenerateFromDescriptionRequest) -> GenerateMusicResponse:
        prompt = self.generate_prompt(request.full_described_song)
        lyrics = ""
        if not request.instrumental:
            lyrics = self.generate_lyrics(request.full_described_song)
        return self.generate_music_with_cover(
            prompt=prompt, 
            lyrics=lyrics,
            description_for_categorization=request.full_described_song, 
            **request.model_dump(exclude={"full_described_song"})
        )

    # @modal.fastapi_endpoint(method="POST", requires_proxy_auth=True)
    @modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
    def generate_with_lyrics(self, request: GenerateWithCustomLyricsRequest) -> GenerateMusicResponse:
        return self.generate_music_with_cover(
            prompt=request.prompt, 
            lyrics=request.lyrics,
            description_for_categorization=request.prompt, 
            **request.model_dump(exclude={"prompt", "lyrics"})
        )

    # @modal.fastapi_endpoint(method="POST", requires_proxy_auth=True)
    @modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
    def generate_with_described_lyrics(self, request: GenerateWithDescribedLyricsRequest) -> GenerateMusicResponse:
        lyrics = ""
        if not request.instrumental:
            lyrics = self.generate_lyrics(request.described_lyrics)
        return self.generate_music_with_cover(
            prompt=request.prompt, 
            lyrics=lyrics,
            description_for_categorization=request.prompt, 
            **request.model_dump(exclude={"described_lyrics", "prompt"})
        )


# =============================================================================
# DEPLOYED ENDPOINT URLs (persistent app - no new containers created)
# =============================================================================
DEPLOYED_ENDPOINTS = {
    # OLD URLs (incorrect - commented for comparison):
    # "generate_with_lyrics": "https://hasratmd697--music-generator-musicgenserver-generate-wlt-ba449d.modal.run",
    # "generate_with_described_lyrics": "https://hasratmd697--music-generator-musicgenserver-generate-wlt-a2ff74.modal.run",
    
    # NEW URLs (correct - from modal deploy output):
    "generate_with_lyrics": "https://hasratmd697--music-generator-musicgenserver-generate-wit-ba449d.modal.run",
    "generate_with_described_lyrics": "https://hasratmd697--music-generator-musicgenserver-generate-wit-a2ff74.modal.run",
    "generate_from_description": "https://hasratmd697--music-generator-musicgenserver-generate-fro-6c1849.modal.run",
}


@app.local_entrypoint()
def main():
    # OLD: Creates a new dev instance every time (commented for comparison)
    # server = MusicGenServer()
    # endpoint_url = server.generate_with_described_lyrics.get_web_url()
    
    # NEW: Use the deployed endpoint directly (no new containers)
    endpoint_url = DEPLOYED_ENDPOINTS["generate_with_described_lyrics"]

    request_data = GenerateWithDescribedLyricsRequest(
        prompt="rave, funk, 140BPM, disco",
        described_lyrics="lyrics about water monsoon",
        guidance_scale=15
    )


    payload = request_data.model_dump()

    response = requests.post(endpoint_url, json=payload)
    response.raise_for_status()
    result = GenerateMusicResponse(**response.json())

    # Save the audio file locally
    audio_bytes = base64.b64decode(result.audio_data)
    with open("generated.wav", "wb") as f:
        f.write(audio_bytes)

    # Save the cover image locally
    image_bytes = base64.b64decode(result.cover_image_data)
    with open("cover.png", "wb") as f:
        f.write(image_bytes)

    print(f"Success! Categories: {result.categories}")
    print("Saved: generated.wav, cover.png")