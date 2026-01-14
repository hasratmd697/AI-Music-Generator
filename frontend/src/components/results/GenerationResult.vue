<script setup>
import { computed, ref } from 'vue';
import { useMusicStore } from '../../stores/musicStore';
import AudioPlayer from '../player/AudioPlayer.vue';
import { ChevronDown, ChevronUp, AlignLeft } from 'lucide-vue-next';

const store = useMusicStore();
const track = computed(() => store.generatedTrack);
const showLyrics = ref(false);

const audioSrc = computed(() => {
    if (!track.value?.audio_data) return null;
    return `data:audio/wav;base64,${track.value.audio_data}`;
});

const coverSrc = computed(() => {
    if (!track.value?.cover_image_data) return null;
    return `data:image/png;base64,${track.value.cover_image_data}`;
});

// Infer title based on mode or categories
const title = computed(() => {
    if (store.mode === 'description') return 'Generated Track';
    if (store.mode === 'lyrics') return 'Custom Song';
    if (store.mode === 'described-lyrics') return 'AI Lyrics Song';
    return 'MusicGen Track';
});

// Attempt to get lyrics.
// Note: Backend currently doesn't return generated lyrics for Mode 1 & 3. 
// We use input lyrics for Mode 2 if available.
const lyricsText = computed(() => {
    if (store.mode === 'lyrics') {
        return store.lyricsForm.lyrics;
    }
    // Future proof: if backend adds lyrics field
    return track.value?.lyrics || null; 
});
</script>

<template>
  <div v-if="track" class="mt-8 animate-in slide-in-from-bottom-4 duration-500">
      <div class="flex items-center gap-2 mb-4">
            <div class="h-px bg-gray-200 dark:bg-gray-800 flex-grow"></div>
            <span class="text-xs uppercase tracking-widest text-gray-400 dark:text-gray-500 font-semibold">Generation Result</span>
            <div class="h-px bg-gray-200 dark:bg-gray-800 flex-grow"></div>
      </div>

    <AudioPlayer 
        :audioUrl="audioSrc"
        :coverUrl="coverSrc"
        :title="title"
        :categories="track.categories"
    />
    
    <!-- Lyrics Section (Collapsible) -->
    <div v-if="lyricsText" class="mt-4 bg-white/50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 rounded-xl overflow-hidden transition-colors duration-300">
        <button 
            @click="showLyrics = !showLyrics"
            class="w-full px-6 py-3 flex justify-between items-center text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
        >
            <div class="flex items-center gap-2">
                <AlignLeft class="w-4 h-4" />
                <span>Lyrics</span>
            </div>
            <component :is="showLyrics ? ChevronUp : ChevronDown" class="w-4 h-4" />
        </button>
        
        <div v-show="showLyrics" class="px-6 pb-6 pt-2">
            <div class="p-4 bg-gray-50 dark:bg-black/30 rounded-lg border border-gray-200 dark:border-white/5 font-mono text-sm text-gray-800 dark:text-gray-300 whitespace-pre-line leading-relaxed">
                {{ lyricsText }}
            </div>
        </div>
    </div>
  </div>
</template>
