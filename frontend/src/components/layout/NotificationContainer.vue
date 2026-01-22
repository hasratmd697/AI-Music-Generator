<script setup>
import { useNotifications } from '../../composables/useNotifications';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle, Loader2 } from 'lucide-vue-next';

const { notifications, removeNotification } = useNotifications();

const icons = {
  success: CheckCircle,
  error: AlertCircle,
  info: Info,
  warning: AlertTriangle,
  loading: Loader2
};

const colors = {
  success: 'bg-green-500 text-white',
  error: 'bg-red-500 text-white',
  info: 'bg-blue-500 text-white',
  warning: 'bg-yellow-500 text-white',
  loading: 'bg-purple-500 text-white'
};
</script>

<template>
  <div class="fixed top-20 right-4 z-[9999] flex flex-col gap-3 max-w-sm w-full pointer-events-none">
    <TransitionGroup 
        enter-active-class="transform ease-out duration-300 transition" 
        enter-from-class="translate-x-full opacity-0" 
        enter-to-class="translate-x-0 opacity-100" 
        leave-active-class="transition ease-in duration-200" 
        leave-from-class="opacity-100" 
        leave-to-class="opacity-0 scale-90"
    >
        <div 
            v-for="notification in notifications" 
            :key="notification.id"
            class="pointer-events-auto rounded-lg shadow-lg overflow-hidden flex items-stretch ring-1 ring-black/5 dark:ring-white/10"
            :class="[
                notification.type === 'error' ? 'bg-red-50 dark:bg-red-900/90 border border-red-200 dark:border-red-800' :
                notification.type === 'success' ? 'bg-green-50 dark:bg-green-900/90 border border-green-200 dark:border-green-800' :
                notification.type === 'loading' ? 'bg-purple-50 dark:bg-purple-900/90 border border-purple-200 dark:border-purple-800' :
                'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
            ]"
        >
            <div class="px-4 py-3 flex items-start gap-3 w-full">
                <component 
                    :is="icons[notification.type]" 
                    class="w-5 h-5 mt-0.5 flex-shrink-0"
                    :class="[
                        notification.type === 'error' ? 'text-red-600 dark:text-red-400' :
                        notification.type === 'success' ? 'text-green-600 dark:text-green-400' :
                        notification.type === 'loading' ? 'text-purple-600 dark:text-purple-400 animate-spin' :
                        'text-gray-500 dark:text-gray-400'
                    ]"
                />
                
                <p class="text-sm font-medium pt-0.5" 
                   :class="[
                       notification.type === 'error' ? 'text-red-800 dark:text-red-200' :
                       notification.type === 'success' ? 'text-green-800 dark:text-green-200' :
                       notification.type === 'loading' ? 'text-purple-800 dark:text-purple-200' :
                       'text-gray-800 dark:text-gray-200'
                   ]">
                    {{ notification.message }}
                </p>

                <button 
                    @click="removeNotification(notification.id)"
                    class="ml-auto text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                >
                    <X class="w-4 h-4" />
                </button>
            </div>
            <!-- Progress bar could be added here -->
        </div>
    </TransitionGroup>
  </div>
</template>
