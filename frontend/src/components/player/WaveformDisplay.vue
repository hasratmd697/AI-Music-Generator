<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import WaveSurfer from 'wavesurfer.js';

const props = defineProps({
  audioUrl: String,
});

const emit = defineEmits(['ready', 'finish']);
const container = ref(null);
let wavesurfer = null;

const initWaveSurfer = () => {
    if (!container.value || wavesurfer) return;

    wavesurfer = WaveSurfer.create({
        container: container.value,
        waveColor: 'rgba(168, 85, 247, 0.5)', // purple-500 optimized
        progressColor: '#ec4899', // pink-500
        cursorColor: '#f3f4f6',
        barWidth: 3,
        barRadius: 3,
        barGap: 2,
        height: 60,
        responsive: true,
        normalize: true,
        hideScrollbar: true,
    });
    
    wavesurfer.on('ready', () => emit('ready'));
    wavesurfer.on('finish', () => emit('finish'));

    if (props.audioUrl) {
        wavesurfer.load(props.audioUrl);
    }
};

watch(() => props.audioUrl, (newUrl) => {
    if (wavesurfer && newUrl) {
        wavesurfer.load(newUrl);
    }
});

onMounted(() => {
    initWaveSurfer();
});

onUnmounted(() => {
    if (wavesurfer) {
        wavesurfer.destroy();
    }
});

defineExpose({
    playPause: () => wavesurfer && wavesurfer.playPause(),
    stop: () => wavesurfer && wavesurfer.stop(),
    setVolume: (v) => wavesurfer && wavesurfer.setVolume(v),
    setPlaybackRate: (rate) => wavesurfer && wavesurfer.setPlaybackRate(rate),
});
</script>

<template>
  <div ref="container" class="w-full"></div>
</template>
