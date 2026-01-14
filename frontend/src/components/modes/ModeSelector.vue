<script setup>
import { useMusicStore } from '../../stores/musicStore';
import { storeToRefs } from 'pinia';

const store = useMusicStore();
const { mode } = storeToRefs(store);

const modes = [
  { id: 'description', label: 'Description' },
  { id: 'lyrics', label: 'Custom Lyrics' },
  { id: 'described-lyrics', label: 'Described Lyrics' },
];

const setMode = (newMode) => {
  store.setMode(newMode);
};
</script>

<template>
  <div class="w-full max-w-md mx-auto mb-8">
    <div class="flex p-1 bg-gray-100 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-inner transition-colors duration-300">
      <button
        v-for="m in modes"
        :key="m.id"
        @click="setMode(m.id)"
        class="flex-1 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 ease-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-gray-900 focus:ring-purple-500"
        :class="[
          mode === m.id
            ? 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white shadow-sm dark:shadow-lg border border-gray-200 dark:border-gray-700/50'
            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-200/50 dark:hover:bg-gray-800/50'
        ]"
      >
        {{ m.label }}
      </button>
    </div>
  </div>
</template>
