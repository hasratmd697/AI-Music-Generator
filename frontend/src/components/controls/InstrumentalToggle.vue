<script setup>
import { Switch } from '@headlessui/vue'

defineProps({
  modelValue: Boolean
})
defineEmits(['update:modelValue'])
</script>

<template>
  <Switch
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', $event)"
    :class="modelValue ? 'bg-purple-600' : 'bg-gray-300 dark:bg-gray-700'"
    class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-gray-900"
  >
    <span class="sr-only">Enable Instrumental Mode</span>
    <span
      :class="modelValue ? 'translate-x-6' : 'translate-x-1'"
      class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
    />
  </Switch>
</template>
