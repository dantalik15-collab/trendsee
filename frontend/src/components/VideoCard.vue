<script setup>
defineProps({
  publication: { type: Object, required: true },
});

defineEmits(["analyze"]);

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}
</script>

<template>
  <div class="vc">
    <div class="vc__preview">
      <img src="/assets/video-preview.png" alt="Video" />
    </div>

    <div class="vc__body">
      <div class="vc__bloger">
        <img src="https://i.pravatar.cc/64?img=47" class="vc__avatar" />
        <div class="vc__info">
          <span class="vc__author">@blogerich</span>
          <span class="vc__subs">384.5K</span>
        </div>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="1.8"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#bbb" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </div>
      <p class="vc__text">{{ publication.title }} — {{ publication.text }}</p>
      <time class="vc__date">{{ formatDate(publication.created_at) }}</time>
      <button class="vc__btn" @click="$emit('analyze', publication)">Анализ</button>
    </div>
  </div>
</template>

<style scoped>
.vc { border-radius: 16px; overflow: hidden; background: #fff; border: 1px solid #f0f0f0; }

.vc__preview { position: relative; aspect-ratio: 9/14; background: #111; }
.vc__preview img { width: 100%; height: 100%; object-fit: cover; display: block; }

.vc__body { padding: 10px 12px 14px; }

.vc__bloger { display: flex; align-items: center; gap: 6px; margin-bottom: 6px; }
.vc__avatar { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.vc__info { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.vc__author { font-size: 12.5px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.vc__subs { font-size: 10.5px; color: #999; }

.vc__text { font-size: 11.5px; color: #333; line-height: 1.4; margin-bottom: 3px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.vc__date { font-size: 10.5px; color: #999; display: block; margin-bottom: 8px; }

.vc__btn { width: 100%; padding: 9px; border: none; border-radius: 10px; background: #4f46e5; color: #fff; font-size: 13px; font-weight: 600; cursor: pointer; font-family: inherit; }
.vc__btn:hover { opacity: 0.9; }
</style>