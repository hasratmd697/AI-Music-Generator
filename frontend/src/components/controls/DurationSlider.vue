<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  min: {
    type: Number,
    default: 1
  },
  max: {
    type: Number,
    default: 300 // 5 minutes max as per api timeout
  },
  step: {
    type: Number,
    default: 1
  }
});

const emit = defineEmits(['update:modelValue']);

// compute percentage for background gradient
const percentage = computed(() => {
    return ((props.modelValue - props.min) / (props.max - props.min)) * 100;
});
</script>

<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-2">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Duration</label>
      <span class="text-sm font-mono text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/30 px-2 py-0.5 rounded font-bold">{{ modelValue }}s</span>
    </div>
    
    <div class="relative w-full h-6 flex items-center">
        <input
          type="range"
          :min="min"
          :max="max"
          :step="step"
          :value="modelValue"
          @input="$emit('update:modelValue', Number($event.target.value))"
          class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-purple-500/50"
          :style="{
              backgroundImage: `linear-gradient(to right, #9333ea ${percentage}%, transparent ${percentage}%)`
          }"
        />
    </div>
    <div class="flex justify-between text-xs text-gray-400 mt-1">
        <span>{{ min }}s</span>
        <span>{{ max }}s</span>
    </div>
  </div>
</template>

<style scoped>
/* Custom thumb styling */
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #ffffff;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(147, 51, 234, 0.5);
  margin-top: -4px; /* Adjust if needed */
}

input[type=range]::-moz-range-thumb {
  height: 16px;
  width: 16px;
  border: none;
  border-radius: 50%;
  background: #ffffff;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(147, 51, 234, 0.5);
}

/* Base track styles handled by bg-gray-700 and linear-gradient in inline-style */
</style>
