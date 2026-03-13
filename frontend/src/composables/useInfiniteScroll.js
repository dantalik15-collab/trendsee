import { ref, onMounted, onUnmounted } from "vue";

const SCROLL_THRESHOLD_PX = 500;

/**
 * Composable для infinite scroll.
 * @param {Function} loadMore — async функция подгрузки следующей порции
 */
export function useInfiniteScroll(loadMore) {
  const loading = ref(false);
  const hasMore = ref(true);

  function onScroll() {
    if (loading.value || !hasMore.value) return;

    const scrollBottom =
      document.documentElement.scrollHeight -
      window.scrollY -
      window.innerHeight;

    if (scrollBottom < SCROLL_THRESHOLD_PX) {
      load();
    }
  }

  async function load() {
    loading.value = true;
    try {
      const more = await loadMore();
      hasMore.value = more;
    } finally {
      loading.value = false;
    }
  }

  onMounted(() => window.addEventListener("scroll", onScroll, { passive: true }));
  onUnmounted(() => window.removeEventListener("scroll", onScroll));

  return { loading, hasMore, load };
}
