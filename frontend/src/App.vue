<script setup>
import { ref } from "vue";
import { fetchPublications } from "./api/publications.js";
import { useInfiniteScroll } from "./composables/useInfiniteScroll.js";
import AppSidebar from "./components/AppSidebar.vue";
import VideoCard from "./components/VideoCard.vue";
import AnalysisPanel from "./components/AnalysisPanel.vue";
import LoadingSpinner from "./components/LoadingSpinner.vue";

const PAGE_SIZE = 20;

const publications = ref([]);
const selectedPublication = ref(null);
const error = ref(null);

async function loadMore() {
  try {
    error.value = null;
    const data = await fetchPublications({
      limit: PAGE_SIZE,
      offset: publications.value.length,
    });
    publications.value.push(...data.items);
    return data.has_more;
  } catch {
    error.value = "Не удалось загрузить публикации";
    return false;
  }
}

const { loading, hasMore, load } = useInfiniteScroll(loadMore);

load();

function openAnalysis(publication) {
  selectedPublication.value = publication;
  document.body.style.overflow = "hidden";
}

function closeAnalysis() {
  selectedPublication.value = null;
  document.body.style.overflow = "";
}
</script>

<template>
  <div class="app">
    <AppSidebar />

    <main class="content">
      <div class="grid">
        <VideoCard
          v-for="pub in publications"
          :key="pub.id"
          :publication="pub"
          @analyze="openAnalysis"
        />
      </div>

      <LoadingSpinner v-if="loading" />

      <p v-if="error" class="content__error">{{ error }}</p>

      <p v-if="!loading && !hasMore && publications.length > 0" class="content__end">
        Все публикации загружены
      </p>

      <p v-if="!loading && !hasMore && publications.length === 0 && !error" class="content__empty">
        Публикаций пока нет. Создайте через Swagger: <a href="http://localhost:8000/docs" target="_blank">localhost:8000/docs</a>
      </p>

      <div v-if="publications.length > 0" class="content__footer">
        <button class="content__footer-btn">⚡ Найти еще ролики</button>
        <div class="content__footer-counter">🕐 Видео: {{ publications.length }} из 3000</div>
      </div>
    </main>

    <AnalysisPanel
      :publication="selectedPublication"
      @close="closeAnalysis"
    />
  </div>
</template>

<style scoped>
.app {
  display: flex;
  min-height: 100vh;
}

.content {
  flex: 1;
  margin-left: var(--sidebar-width);
  padding: 20px 24px 40px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

@media (max-width: 1400px) { .grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 1080px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 700px) {
  .content { margin-left: 0; padding: 12px; }
  .grid { grid-template-columns: 1fr; max-width: 360px; margin: 0 auto; }
}

.content__error { text-align: center; color: #e44; padding: 16px; font-size: 14px; }
.content__end, .content__empty { text-align: center; color: #999; padding: 24px 0; font-size: 13px; }
.content__empty a { color: var(--color-accent); }

.content__footer { display: flex; justify-content: center; align-items: center; gap: 20px; padding: 28px 0; }
.content__footer-btn { padding: 11px 24px; border: none; border-radius: 12px; background: var(--color-accent); color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; font-family: inherit; }
.content__footer-btn:hover { opacity: 0.9; }
.content__footer-counter { padding: 9px 18px; border-radius: 12px; background: #1a1a2e; color: #fff; font-size: 13px; font-weight: 500; }
</style>
