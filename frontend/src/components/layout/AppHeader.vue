<script setup>
import { Music } from 'lucide-vue-next';
import { onMounted } from 'vue';

// Always use dark mode
onMounted(() => {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
});
</script>

<template>
  <header class="bg-gray-900/80 backdrop-blur-md border-b border-gray-800 text-white py-4 px-6 flex justify-between items-center sticky top-0 z-50 shadow-lg">
    <div class="flex items-center gap-3">
      <div class="p-2 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg shadow-purple-500/20 shadow-lg">
        <Music class="w-6 h-6 text-white" />
      </div>
      <h1 class="text-xl font-bold tracking-tight">
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">AI Music</span>
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500 ml-1">Generator</span>
      </h1>
    </div>
  </header>
</template>
