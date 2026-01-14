<script setup>
import { Moon, Sun, Music } from 'lucide-vue-next';
import { ref, onMounted } from 'vue';

const isDark = ref(true);

const toggleDarkMode = () => {
    isDark.value = !isDark.value;
    updateTheme();
}

const updateTheme = () => {
    if (isDark.value) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    }
}

onMounted(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        isDark.value = savedTheme === 'dark';
    } else {
        // Default to dark
        isDark.value = true;
    }
    updateTheme();
});
</script>

<template>
  <header class="bg-gray-900/80 backdrop-blur-md border-b border-gray-800 text-white py-4 px-6 flex justify-between items-center sticky top-0 z-50 shadow-lg transition-colors duration-300 dark:bg-gray-900/80 dark:border-gray-800 bg-white/80 border-gray-200">
    <div class="flex items-center gap-3">
      <div class="p-2 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg shadow-purple-500/20 shadow-lg">
        <Music class="w-6 h-6 text-white" />
      </div>
      <h1 class="text-xl font-bold tracking-tight">
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-gray-800 to-gray-500 dark:from-white dark:to-gray-400">AI Music</span>
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-500 ml-1">Generator</span>
      </h1>
    </div>
    
    <button 
        @click="toggleDarkMode"
        class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-white/5 transition-colors border border-transparent hover:border-gray-200 dark:hover:border-white/10"
    >
      <Sun v-if="!isDark" class="w-5 h-5 text-yellow-500" />
      <Moon v-else class="w-5 h-5 text-purple-300" />
    </button>
  </header>
</template>
