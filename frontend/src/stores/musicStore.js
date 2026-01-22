import { defineStore } from 'pinia';
import api, { ENDPOINTS } from '../services/api';
import { useNotifications } from '../composables/useNotifications';

export const useMusicStore = defineStore('music', {
  state: () => ({
    isLoading: false,
    error: null,
    generatedTrack: null, // { audio: base64, cover: base64, lyrics: string, ... }
    
    // Form States
    mode: 'description', // 'description', 'lyrics', 'described-lyrics'
    
    // Mode 1: Description
    descriptionForm: {
      text: '',
      isInstrumental: false,
      duration: 30,
      seed: -1,
      guidanceScale: 15,
    },
    
    // Mode 2: Custom Lyrics
    lyricsForm: {
      prompt: '',
      lyrics: '',
      duration: 30,
      seed: -1,
      guidanceScale: 15,
    },
    
    // Mode 3: Described Lyrics
    describedLyricsForm: {
      prompt: '',
      lyricsDescription: '',
      duration: 30,
      seed: -1,
      guidanceScale: 15,
    },
  }),

  actions: {
    async generateMusic() {
      this.isLoading = true;
      this.error = null;
      this.generatedTrack = null;

      // Show loading notification (persists until removed)
      const { loading, removeNotification, success, error } = useNotifications();
      const loadingNotificationId = loading("🎵 Generating your music... This takes about 60 seconds.");

      try {
        let endpoint = '';
        let payload = {};
        
        if (this.mode === 'description') {
          endpoint = ENDPOINTS.generateFromDescription;
          payload = {
            full_described_song: this.descriptionForm.text,
            instrumental: this.descriptionForm.isInstrumental,
            audio_duration: this.descriptionForm.duration,
            seed: this.descriptionForm.seed,
            guidance_scale: this.descriptionForm.guidanceScale,
          };
        } else if (this.mode === 'lyrics') {
          endpoint = ENDPOINTS.generateWithLyrics;
           payload = {
            prompt: this.lyricsForm.prompt,
            lyrics: this.lyricsForm.lyrics,
            audio_duration: this.lyricsForm.duration,
            seed: this.lyricsForm.seed,
            guidance_scale: this.lyricsForm.guidanceScale,
            instrumental: false, 
          };
        } else if (this.mode === 'described-lyrics') {
          endpoint = ENDPOINTS.generateWithDescribedLyrics;
          payload = {
            prompt: this.describedLyricsForm.prompt,
            described_lyrics: this.describedLyricsForm.lyricsDescription,
            audio_duration: this.describedLyricsForm.duration,
            seed: this.describedLyricsForm.seed,
            guidance_scale: this.describedLyricsForm.guidanceScale,
            instrumental: false,
          };
        }

        const response = await api.post(endpoint, payload);
        this.generatedTrack = response.data;
        
        // Remove loading notification and show success
        removeNotification(loadingNotificationId);
        success("🎉 Your music is ready! Scroll down to listen.");
      } catch (err) {
        console.error("Generation failed:", err);
        const errorMsg = err.response?.data?.detail || err.message || "Failed to generate music";
        this.error = errorMsg;
        
        // Remove loading notification and show error
        removeNotification(loadingNotificationId);
        error(errorMsg);
      } finally {
        this.isLoading = false;
      }
    },

    setMode(mode) {
      this.mode = mode;
    },
    
    resetResult() {
        this.generatedTrack = null;
        this.error = null;
    }
  },
});
