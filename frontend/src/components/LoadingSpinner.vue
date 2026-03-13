<template>
  <div class="spinner">
    <div class="spinner__dot" />
    <div class="spinner__dot" />
    <div class="spinner__dot" />
  </div>
</template>

<style scoped>
.spinner { display: flex; justify-content: center; gap: 8px; padding: 24px 0; }
.spinner__dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-accent); animation: bounce 1.2s ease-in-out infinite; }
.spinner__dot:nth-child(2) { animation-delay: 0.15s; }
.spinner__dot:nth-child(3) { animation-delay: 0.3s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
</style>
