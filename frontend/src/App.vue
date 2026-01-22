<script setup>
import AppHeader from './components/layout/AppHeader.vue';
import AppFooter from './components/layout/AppFooter.vue';
import ModeSelector from './components/modes/ModeSelector.vue';
import DescriptionMode from './components/modes/DescriptionMode.vue';
import LyricsMode from './components/modes/LyricsMode.vue';
import DescribedLyricsMode from './components/modes/DescribedLyricsMode.vue';
import GenerationResult from './components/results/GenerationResult.vue';
import NotificationContainer from './components/layout/NotificationContainer.vue';
import { useMusicStore } from './stores/musicStore';
import { storeToRefs } from 'pinia';
import { Music } from 'lucide-vue-next';

const store = useMusicStore();
const { mode } = storeToRefs(store);
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-white flex flex-col font-sans selection:bg-purple-500/30 relative overflow-hidden transition-colors duration-300">
    <!-- Background Gradient Blobs -->
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
       <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-200/40 dark:bg-purple-900/20 rounded-full blur-[120px] mix-blend-multiply dark:mix-blend-screen opacity-50 animate-pulse-slow"></div>
       <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-200/40 dark:bg-blue-900/20 rounded-full blur-[120px] mix-blend-multiply dark:mix-blend-screen opacity-50 animate-pulse-slow"></div>
    </div>

    <AppHeader />
    <NotificationContainer />
    
    <main class="flex-grow container mx-auto px-4 py-8 max-w-5xl relative z-10">
      <ModeSelector />
      
      <div class="bg-white/60 dark:bg-gray-900/60 backdrop-blur-xl rounded-2xl border border-gray-200 dark:border-gray-800/60 p-1 shadow-2xl ring-1 ring-black/5 dark:ring-white/5 transition-colors duration-300">
        <div class="bg-white/40 dark:bg-gray-900/40 rounded-xl p-6 min-h-[400px] transition-colors duration-300">
          <!-- Generation status is now shown via toast notifications (see NotificationContainer) -->
          <!-- Users can continue browsing while music generates in the background -->

          <Transition
            mode="out-in"
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 translate-y-4"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 translate-y-4"
          >
             <component 
                :is="mode === 'description' ? DescriptionMode : mode === 'lyrics' ? LyricsMode : DescribedLyricsMode" 
                :key="mode"
             />
          </Transition>
        </div>
      </div>

      <GenerationResult />
    </main>
    
    <AppFooter />
  </div>
</template>

<style>
@keyframes pulse-slow {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.7; }
}
.animate-pulse-slow {
  animation: pulse-slow 8s infinite ease-in-out;
}
</style>
