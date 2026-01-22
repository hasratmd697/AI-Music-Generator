"""
AI Music Generator - Backend Server

This module implements a Modal-based serverless backend for AI music generation.
It integrates multiple AI models to create music from text descriptions:
    - ACE-Step: For generating music audio from prompts and lyrics
    - Qwen2-7B: For generating lyrics and music prompts from descriptions
    - SDXL-Turbo: For generating album cover art

The server exposes FastAPI endpoints for different music generation workflows.

Author: Hasrat MD
Created: 2026
"""

import base64
import os
from typing import List
import uuid
import modal
from pydantic import BaseModel
import requests

from prompts import LYRICS_GENERATOR_PROMPT, PROMPT_GENERATOR_PROMPT

# =============================================================================
# Modal App Configuration
# =============================================================================

# Initialize the Modal application with a unique identifier
app = modal.App("music-generator")

# Define the Docker image with all required dependencies
# This image will be used for running the music generation server
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg",)  # ffmpeg for audio processing
    .pip_install_from_requirements("requirements.txt")
    .run_commands([
        # Clone and install the ACE-Step music generation model
        "git clone https://github.com/ace-step/ACE-Step.git /tmp/ACE-Step",
        "cd /tmp/ACE-Step && pip install .",
        "pip install torchcodec"  # Required for audio encoding/decoding
    ])
    .env({"HF_HOME": "/.cache/huggingface"})  # Set HuggingFace cache directory
    .add_local_python_source("prompts")  # Include prompts module
)

# =============================================================================
# Modal Volumes for Model Persistence
# =============================================================================

# Volume for storing ACE-Step model weights (persists across container restarts)
model_volume = modal.Volume.from_name(
    "ace-step-models", create_if_missing=True)

# Volume for caching HuggingFace models (Qwen LLM and SDXL)
hf_volume = modal.Volume.from_name("qwen-hf-cache", create_if_missing=True)

# Secrets for API authentication (if needed)
music_gen_secrets = modal.Secret.from_name("music-gen-secret")


# =============================================================================
# Request/Response Data Models (Pydantic Schemas)
# =============================================================================

class AudioGenerationBase(BaseModel):
    """
    Base configuration for all audio generation requests.
    
    Attributes:
        audio_duration: Length of generated audio in seconds (default: 180s = 3 min)
        seed: Random seed for reproducibility (-1 for random)
        guidance_scale: CFG scale for generation quality (higher = closer to prompt)
        infer_step: Number of inference steps (higher = better quality, slower)
        instrumental: If True, generate instrumental-only music (no vocals)
    """
    audio_duration: float = 180.0
    seed: int = -1
    guidance_scale: float = 15.0
    infer_step: int = 60
    instrumental: bool = False


class GenerateFromDescriptionRequest(AudioGenerationBase):
    """
    Request schema for generating music from a full description.
    The system will auto-generate both the prompt and lyrics from this description.
    
    Attributes:
        full_described_song: Complete description of the desired song
                            (e.g., "An upbeat summer pop song about road trips")
    """
    full_described_song: str


class GenerateWithCustomLyricsRequest(AudioGenerationBase):
    """
    Request schema for generating music with user-provided lyrics.
    
    Attributes:
        prompt: Music style/genre description (e.g., "pop, upbeat, 120BPM")
        lyrics: User-written lyrics to be sung in the generated song
    """
    prompt: str
    lyrics: str


class GenerateWithDescribedLyricsRequest(AudioGenerationBase):
    """
    Request schema for generating music with AI-generated lyrics.
    
    Attributes:
        prompt: Music style/genre description (e.g., "rave, funk, 140BPM")
        described_lyrics: Description of lyric theme for AI to generate
                         (e.g., "lyrics about summer love and beaches")
    """
    prompt: str
    described_lyrics: str


class GenerateMusicResponse(BaseModel):
    """
    Response schema for all music generation endpoints.
    
    Attributes:
        audio_data: Base64-encoded WAV audio data
        cover_image_data: Base64-encoded PNG album cover image
        categories: List of genre/mood tags for the generated music
    """
    audio_data: str  # base64 encoded audio
    cover_image_data: str  # base64 encoded image
    categories: List[str]


# =============================================================================
# Music Generation Server Class
# =============================================================================

@app.cls(
    image=image,
    gpu="L40S",  # NVIDIA L40S GPU for fast inference
    volumes={"/models": model_volume, "/.cache/huggingface": hf_volume},
    secrets=[music_gen_secrets],
    scaledown_window=15  # Keep container warm for 15 seconds after last request
)
class MusicGenServer:
    """
    Modal server class that handles music generation requests.
    
    This class loads and manages three AI models:
    1. ACE-Step: Music generation model
    2. Qwen2-7B: LLM for generating prompts and lyrics
    3. SDXL-Turbo: Image generation for album covers
    
    The @modal.enter() decorator ensures models are loaded once when
    the container starts, not on every request.
    """
    
    @modal.enter()
    def load_model(self):
        """
        Initialize and load all AI models into GPU memory.
        This method runs once when the container starts.
        """
        from acestep.pipeline_ace_step import ACEStepPipeline
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from diffusers import AutoPipelineForText2Image
        import torch

        # Music Generation Model (ACE-Step)
        # Loads checkpoint from persistent volume to avoid re-downloading
        self.music_model = ACEStepPipeline(
            checkpoint_dir="/models",
            dtype="bfloat16",  # Use BF16 for memory efficiency
            torch_compile=False,
            cpu_offload=False,
            overlapped_decode=False
        )

        # Large Language Model (Qwen2-7B-Instruct)
        # Used for generating lyrics and music prompts from descriptions
        model_id = "Qwen/Qwen2-7B-Instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        self.llm_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto",  # Automatically distribute across available GPUs
            cache_dir="/.cache/huggingface"
        )

        # Stable Diffusion Model (SDXL-Turbo)
        # Used for generating album cover thumbnails quickly
        self.image_pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=torch.float16, 
            variant="fp16", 
            cache_dir="/.cache/huggingface"
        )
        self.image_pipe.to("cuda")

    # -------------------------------------------------------------------------
    # LLM Utility Methods
    # -------------------------------------------------------------------------

    def prompt_qwen(self, question: str) -> str:
        """
        Send a prompt to the Qwen LLM and get a response.
        
        Args:
            question: The prompt/question to send to the LLM
            
        Returns:
            The LLM's text response
        """
        messages = [
            {"role": "user", "content": question}
        ]
        
        # Apply chat template for proper formatting
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Tokenize and move to model device
        model_inputs = self.tokenizer(
            [text], return_tensors="pt").to(self.llm_model.device)

        # Generate response
        generated_ids = self.llm_model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        
        # Extract only the new tokens (exclude input tokens)
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        # Decode tokens to text
        response = self.tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True)[0]

        return response

    def generate_prompt(self, description: str) -> str:
        """
        Generate a music-specific prompt from a general description.
        
        Args:
            description: User's description of the desired song
            
        Returns:
            Formatted music generation prompt with style tags
        """
        full_prompt = PROMPT_GENERATOR_PROMPT.format(user_prompt=description)
        return self.prompt_qwen(full_prompt)

    def generate_lyrics(self, description: str) -> str:
        """
        Generate song lyrics based on a thematic description.
        
        Args:
            description: Description of the lyrics theme/content
            
        Returns:
            Generated song lyrics in proper verse/chorus format
        """
        full_prompt = LYRICS_GENERATOR_PROMPT.format(description=description)
        return self.prompt_qwen(full_prompt)

    def generate_categories(self, description: str) -> List[str]:
        """
        Generate genre/mood categories for the music based on description.
        
        Args:
            description: Description of the music
            
        Returns:
            List of 3-5 relevant genre/mood tags (e.g., ["Pop", "Electronic", "Upbeat"])
        """
        prompt = f"Based on the following music description, list 3-5 relevant genres or categories as a comma-separated list. For example: Pop, Electronic, Sad, 80s. Description: '{description}'"
        response_text = self.prompt_qwen(prompt)
        categories = [cat.strip() for cat in response_text.split(",") if cat.strip()]
        return categories

    # -------------------------------------------------------------------------
    # Core Music Generation Method
    # -------------------------------------------------------------------------

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
        """
        Core method that generates music audio, album cover, and categories.
        
        Args:
            prompt: Music style/genre prompt for the ACE-Step model
            lyrics: Song lyrics (or empty for instrumental)
            instrumental: If True, generate instrumental-only
            audio_duration: Length of audio in seconds
            infer_step: Number of diffusion inference steps
            guidance_scale: Classifier-free guidance scale
            seed: Random seed for reproducibility
            description_for_categorization: Text used to generate category tags
            
        Returns:
            GenerateMusicResponse with base64-encoded audio, image, and categories
        """
        import io

        # Use instrumental placeholder if no vocals needed
        final_lyrics = "[instrumental]" if instrumental else lyrics
        print(f"Generated lyrics: \n{final_lyrics}")
        print(f"Prompt: \n{prompt}")

        # Create temporary output directory for audio file
        output_dir = "/tmp/outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")

        # Generate music using ACE-Step model
        self.music_model(
            prompt=prompt,
            lyrics=final_lyrics,
            audio_duration=audio_duration,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            save_path=output_path,
            manual_seeds=str(seed)
        )

        # Read generated audio and encode to base64
        with open(output_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        os.remove(output_path)  # Clean up temporary file

        # Generate album cover thumbnail using SDXL-Turbo
        thumbnail_prompt = f"{prompt}, album cover art"
        image = self.image_pipe(
            prompt=thumbnail_prompt, 
            num_inference_steps=2,  # SDXL-Turbo only needs 1-4 steps
            guidance_scale=0.0  # Turbo models work best with 0 guidance
        ).images[0]

        # Encode cover image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        image_b64 = base64.b64encode(img_buffer.read()).decode("utf-8")

        # Generate category tags for the music
        categories = self.generate_categories(description_for_categorization)

        return GenerateMusicResponse(
            audio_data=audio_b64,
            cover_image_data=image_b64,
            categories=categories
        )

    # -------------------------------------------------------------------------
    # FastAPI Endpoint Methods
    # -------------------------------------------------------------------------

    # NOTE: requires_proxy_auth=False for development; set to True for production
    @modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
    def generate_from_description(self, request: GenerateFromDescriptionRequest) -> GenerateMusicResponse:
        """
        API Endpoint: Generate music from a full description.
        
        The system automatically generates both the music prompt and lyrics
        from the provided description.
        
        Args:
            request: Contains full_described_song and generation parameters
            
        Returns:
            GenerateMusicResponse with audio, cover image, and categories
        """
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

    @modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
    def generate_with_lyrics(self, request: GenerateWithCustomLyricsRequest) -> GenerateMusicResponse:
        """
        API Endpoint: Generate music with user-provided lyrics.
        
        Uses the user's custom lyrics directly without AI generation.
        
        Args:
            request: Contains prompt, lyrics, and generation parameters
            
        Returns:
            GenerateMusicResponse with audio, cover image, and categories
        """
        return self.generate_music_with_cover(
            prompt=request.prompt, 
            lyrics=request.lyrics,
            description_for_categorization=request.prompt, 
            **request.model_dump(exclude={"prompt", "lyrics"})
        )

    @modal.fastapi_endpoint(method="POST", requires_proxy_auth=False)
    def generate_with_described_lyrics(self, request: GenerateWithDescribedLyricsRequest) -> GenerateMusicResponse:
        """
        API Endpoint: Generate music with AI-generated lyrics.
        
        The lyrics are generated by the LLM based on the provided description.
        
        Args:
            request: Contains prompt, described_lyrics, and generation parameters
            
        Returns:
            GenerateMusicResponse with audio, cover image, and categories
        """
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
# Deployed Endpoint URLs
# =============================================================================
# These are the permanent URLs for the deployed Modal app.
# Use these to call the endpoints without spinning up new containers.

DEPLOYED_ENDPOINTS = {
    "generate_with_lyrics": "https://hasratmd697--music-generator-musicgenserver-generate-wit-ba449d.modal.run",
    "generate_with_described_lyrics": "https://hasratmd697--music-generator-musicgenserver-generate-wit-a2ff74.modal.run",
    "generate_from_description": "https://hasratmd697--music-generator-musicgenserver-generate-fro-6c1849.modal.run",
}


# =============================================================================
# Local Development Entry Point
# =============================================================================

@app.local_entrypoint()
def main():
    """
    Local entry point for testing the deployed endpoints.
    
    This function demonstrates how to call the deployed music generation
    API from a local script. It sends a request to generate music and
    saves the resulting audio and cover image to local files.
    
    Usage:
        modal run main.py
    """
    # Use the deployed endpoint (doesn't create new containers)
    endpoint_url = DEPLOYED_ENDPOINTS["generate_with_described_lyrics"]

    # Create a sample request for testing
    request_data = GenerateWithDescribedLyricsRequest(
        prompt="rave, funk, 140BPM, disco",
        described_lyrics="lyrics about water monsoon",
        guidance_scale=15
    )

    # Convert request to JSON and send to API
    payload = request_data.model_dump()

    response = requests.post(endpoint_url, json=payload)
    response.raise_for_status()  # Raise exception for HTTP errors
    result = GenerateMusicResponse(**response.json())

    # Save the generated audio file locally
    audio_bytes = base64.b64decode(result.audio_data)
    with open("generated.wav", "wb") as f:
        f.write(audio_bytes)

    # Save the album cover image locally
    image_bytes = base64.b64decode(result.cover_image_data)
    with open("cover.png", "wb") as f:
        f.write(image_bytes)

    # Print success message with generated categories
    print(f"Success! Categories: {result.categories}")
    print("Saved: generated.wav, cover.png")