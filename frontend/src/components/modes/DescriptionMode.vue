<script setup>
import { useMusicStore } from '../../stores/musicStore';
import { storeToRefs } from 'pinia';
import InstrumentalToggle from '../controls/InstrumentalToggle.vue';
import DurationSlider from '../controls/DurationSlider.vue';
import AdvancedSettings from '../controls/AdvancedSettings.vue';
import { Sparkles, Loader2 } from 'lucide-vue-next';

const store = useMusicStore();
const { descriptionForm, isLoading } = storeToRefs(store);

const generate = () => {
    if(!descriptionForm.value.text.trim()) return;
    store.generateMusic();
};
</script>

<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <!-- Description Input -->
    <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Describe your song
            <span class="text-gray-500 dark:text-gray-500 font-normal ml-2">(style, mood, instruments)</span>
        </label>
        <textarea
            v-model="descriptionForm.text"
            rows="4"
            class="w-full bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl p-4 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-all resize-none shadow-sm dark:shadow-inner"
            placeholder="A nostalgic 80s synthwave track with driving bass and neon aesthetic..."
        ></textarea>
        <!-- Quick Tags (Optional Idea, sticking to plan simple form first) -->
    </div>

    <!-- Main Controls -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
        <DurationSlider v-model="descriptionForm.duration" />
        
        <div class="flex items-center justify-between bg-gray-50 dark:bg-gray-800/30 p-3 rounded-lg border border-gray-200 dark:border-gray-700/50">
            <div class="flex flex-col">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Instrumental</span>
                <span class="text-xs text-gray-500">No lyrics generation</span>
            </div>
            <InstrumentalToggle v-model="descriptionForm.isInstrumental" />
        </div>
    </div>

    <!-- Advanced Settings -->
    <AdvancedSettings :formState="descriptionForm" />

    <!-- Action Button -->
    <button
        @click="generate"
        :disabled="isLoading || !descriptionForm.text.trim()"
        class="w-full py-4 px-6 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 shadow-lg shadow-purple-900/20"
        :class="isLoading ? 'bg-gray-700 text-gray-400' : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white'"
    >
        <Loader2 v-if="isLoading" class="w-6 h-6 animate-spin" />
        <Sparkles v-else class="w-6 h-6" />
        {{ isLoading ? 'Generating Music...' : 'Generate Music' }}
    </button>
  </div>
</template>
