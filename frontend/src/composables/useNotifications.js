import { ref } from "vue";

const notifications = ref([]);
let counter = 0;

export function useNotifications() {
  const addNotification = (type, message, duration = 5000) => {
    const id = counter++;
    notifications.value.push({ id, type, message });

    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }

    return id; // Return ID for manual removal
  };

  const removeNotification = (id) => {
    notifications.value = notifications.value.filter((n) => n.id !== id);
  };

  const success = (message) => addNotification("success", message);
  const error = (message) => addNotification("error", message);
  const info = (message) => addNotification("info", message);
  const warning = (message) => addNotification("warning", message);

  // Loading notification - persists until manually removed, returns ID
  const loading = (message) => addNotification("loading", message, 0);

  return {
    notifications,
    addNotification,
    removeNotification,
    success,
    error,
    info,
    warning,
    loading,
  };
}
