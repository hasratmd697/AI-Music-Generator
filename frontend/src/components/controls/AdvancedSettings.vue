<script setup>
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { ChevronUp, Settings } from 'lucide-vue-next'

const props = defineProps({
  formState: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="w-full">
    <Disclosure v-slot="{ open }">
      <DisclosureButton
        class="flex w-full justify-between rounded-lg bg-gray-100 dark:bg-gray-800 px-4 py-2 text-left text-sm font-medium text-purple-900 dark:text-purple-200 hover:bg-gray-200 dark:hover:bg-gray-700/80 focus:outline-none focus-visible:ring focus-visible:ring-purple-500 focus-visible:ring-opacity-75 transition-colors"
      >
        <div class="flex items-center gap-2">
            <Settings class="w-4 h-4" />
            <span>Advanced Settings</span>
        </div>
        <ChevronUp
          :class="open ? 'rotate-180 transform' : ''"
          class="h-5 w-5 text-purple-500 dark:text-purple-300 transition-transform duration-200"
        />
      </DisclosureButton>
      <transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-75 ease-out"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
      >
        <DisclosurePanel class="px-4 pt-4 pb-2 text-sm text-gray-600 dark:text-gray-400 space-y-4">
            <!-- Seed Input -->
            <div>
                <label class="block mb-1 text-xs uppercase tracking-wider font-semibold text-gray-500">Seed</label>
                <div class="flex gap-2">
                    <input 
                        type="number" 
                        v-model="formState.seed" 
                        class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded px-3 py-2 text-gray-900 dark:text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-colors shadow-sm dark:shadow-inner"
                        placeholder="-1 for random" 
                    />
                    <button 
                        @click="formState.seed = -1"
                        class="px-3 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 transition-colors"
                        title="Reset to Random"
                    >
                        Random
                    </button>
                </div>
                <p class="mt-1 text-xs text-gray-500 dark:text-gray-600">Use -1 for random generation.</p>
            </div>

            <!-- Guidance Scale Input -->
            <div>
                <div class="flex justify-between mb-1">
                    <label class="text-xs uppercase tracking-wider font-semibold text-gray-500">Guidance Scale</label>
                    <span class="text-xs font-mono text-purple-600 dark:text-purple-400">{{ formState.guidanceScale }}</span>
                </div>
                <input 
                    type="range" 
                    v-model.number="formState.guidanceScale" 
                    min="1" 
                    max="30" 
                    step="0.5"
                    class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
                <p class="mt-1 text-xs text-gray-500 dark:text-gray-600">Higher values follow the prompt more strictly.</p>
            </div>
        </DisclosurePanel>
      </transition>
    </Disclosure>
  </div>
</template>
