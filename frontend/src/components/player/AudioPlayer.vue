<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import WaveformDisplay from './WaveformDisplay.vue';
import { Play, Pause, Download, Volume2, Share2 } from 'lucide-vue-next';

const props = defineProps({
  audioUrl: {
      type: String, 
      required: true
  },
  coverUrl: String,
  title: {
      type: String,
      default: 'Generated Track'
  },
  categories: {
      type: Array,
      default: () => []
  }
});

const isPlaying = ref(false);
const waveformRef = ref(null);
const playbackSpeed = ref(1.0);

const setSpeed = (rate) => {
    playbackSpeed.value = rate;
    if (waveformRef.value) {
        waveformRef.value.setPlaybackRate(rate);
    }
};

const togglePlay = () => {
    if (waveformRef.value) {
        waveformRef.value.playPause();
        isPlaying.value = !isPlaying.value;
    }
};

const onFinish = () => {
    isPlaying.value = false;
};

// Handle download
const downloadAudio = () => {
    const link = document.createElement('a');
    link.href = props.audioUrl;
    link.download = `generated-${Date.now()}.wav`;
    link.click();
};

// If audio url changes, reset playing state
watch(() => props.audioUrl, () => {
    isPlaying.value = false;
}, { immediate: true });
</script>

<template>
  <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-xl dark:shadow-2xl relative overflow-hidden group transition-all duration-300">
    <!-- Glow Effect -->
    <div class="absolute -top-10 -right-10 w-32 h-32 bg-purple-200/50 dark:bg-purple-600/20 blur-[60px] rounded-full pointer-events-none group-hover:bg-purple-300/50 dark:group-hover:bg-purple-600/30 transition-all duration-500"></div>

    <div class="flex flex-col md:flex-row gap-6 relative z-10">
        <!-- Cover Art -->
        <div class="w-full md:w-32 md:h-32 rounded-lg bg-gray-100 dark:bg-gray-800 shadow-lg overflow-hidden flex-shrink-0 border border-gray-200 dark:border-gray-700">
            <img 
                v-if="coverUrl" 
                :src="coverUrl" 
                class="w-full h-full object-cover transform transition-transform duration-500 hover:scale-110" 
                alt="Album Cover" 
            />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400 dark:text-gray-600">
                <Music class="w-10 h-10" />
            </div>
        </div>
        
        <!-- Controls & Waveform -->
        <div class="flex-grow flex flex-col justify-between py-1">
            <div class="flex justify-between items-start mb-4">
                <div>
                     <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">{{ title }}</h3>
                     <div class="flex flex-wrap gap-2">
                         <span v-for="cat in categories" :key="cat" class="text-xs px-2 py-0.5 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-300 border border-purple-200 dark:border-purple-500/20">
                             {{ cat }}
                         </span>
                     </div>
                </div>
                
                <div class="flex gap-2">
                     <button @click="downloadAudio" class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-full transition-colors" title="Download Audio">
                         <Download class="w-5 h-5" />
                     </button>
                     <button class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-full transition-colors" title="Share (Coming Soon)">
                         <Share2 class="w-5 h-5" />
                     </button>
                </div>
            </div>
            
            <div class="flex items-center gap-4">
                <button 
                  @click="togglePlay"
                  class="w-12 h-12 rounded-full flex items-center justify-center bg-gray-900 dark:bg-white text-white dark:text-black hover:scale-105 active:scale-95 transition-all shadow-lg shadow-black/10 dark:shadow-white/10"
                >
                  <Pause v-if="isPlaying" class="w-5 h-5 fill-current" />
                  <Play v-else class="w-5 h-5 fill-current translate-x-0.5" />
                </button>
                
                <div class="flex-grow h-16 bg-gray-50 dark:bg-gray-800/50 rounded-lg p-2 border border-gray-200 dark:border-white/5">
                     <WaveformDisplay 
                        ref="waveformRef" 
                        :audioUrl="audioUrl" 
                        @finish="onFinish"
                     />
                </div>

                <!-- Playback Speed Control -->
                <div class="relative group">
                    <button class="flex items-center gap-1 px-2 py-1 text-xs font-mono font-bold text-gray-500 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors bg-gray-100 dark:bg-gray-800 rounded">
                        {{ playbackSpeed }}x
                    </button>
                    <div class="absolute bottom-full right-0 mb-2 w-24 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden hidden group-hover:block z-20">
                        <button 
                            v-for="rate in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]" 
                            :key="rate"
                            @click="setSpeed(rate)"
                            class="w-full px-3 py-2 text-left text-sm hover:bg-purple-50 dark:hover:bg-purple-900/20 text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-300 transition-colors flex justify-between"
                        >
                            {{ rate }}x
                            <span v-if="playbackSpeed === rate" class="text-purple-500">•</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
