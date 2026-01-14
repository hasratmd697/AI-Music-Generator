<script setup>
import { useMusicStore } from '../../stores/musicStore';
import { storeToRefs } from 'pinia';
import DurationSlider from '../controls/DurationSlider.vue';
import AdvancedSettings from '../controls/AdvancedSettings.vue';
import { Sparkles, Loader2, Music, PenTool } from 'lucide-vue-next';

const store = useMusicStore();
const { describedLyricsForm, isLoading } = storeToRefs(store);

const generate = () => {
    if(!describedLyricsForm.value.prompt.trim() || !describedLyricsForm.value.lyricsDescription.trim()) return;
    store.generateMusic();
};
</script>

<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <!-- Music Style Input -->
    <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Music Style</label>
        <div class="relative">
            <Music class="absolute left-3 top-3 w-5 h-5 text-gray-400 dark:text-gray-500" />
            <input
                type="text"
                v-model="describedLyricsForm.prompt"
                class="w-full bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl pl-10 pr-4 py-3 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-all shadow-sm dark:shadow-inner"
                placeholder="Sad piano ballad, slow tempo"
            />
        </div>
    </div>

    <!-- Lyrics Description Input -->
    <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Lyrics Topic</label>
         <div class="relative">
             <PenTool class="absolute left-3 top-3 w-5 h-5 text-gray-400 dark:text-gray-500" />
            <textarea
                v-model="describedLyricsForm.lyricsDescription"
                rows="4"
                class="w-full bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl pl-10 pr-4 py-3 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-all resize-none shadow-sm dark:shadow-inner"
                placeholder="A song about losing a friend but finding hope in memories..."
            ></textarea>
        </div>
    </div>

    <DurationSlider v-model="describedLyricsForm.duration" />
    
    <AdvancedSettings :formState="describedLyricsForm" />

    <button
        @click="generate"
        :disabled="isLoading || !describedLyricsForm.prompt.trim() || !describedLyricsForm.lyricsDescription.trim()"
        class="w-full py-4 px-6 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-lg shadow-purple-900/20"
        :class="isLoading ? 'bg-gray-700 text-gray-400' : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white'"
    >
        <Loader2 v-if="isLoading" class="w-6 h-6 animate-spin" />
        <Sparkles v-else class="w-6 h-6" />
        {{ isLoading ? 'Generating Music...' : 'Generate with AI Lyrics' }}
    </button>
  </div>
</template>
