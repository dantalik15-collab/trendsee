<script setup>
const props = defineProps({
  publication: { type: Object, default: null },
});

defineEmits(["close"]);

function formatDateTime(iso) {
  return new Date(iso).toLocaleString("ru-RU", {
    day: "numeric", month: "long", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

const tags = [
  { label: "Туториал", cls: "tag--orange" },
  { label: "Энергичное видео", cls: "tag--green" },
  { label: "Изи монтаж", cls: "tag--indigo" },
  { label: "Трендовый звук", cls: "tag--indigo" },
  { label: "Лид магнит", cls: "tag--orange" },
  { label: "Красота и здоровье", cls: "tag--orange" },
];

const stats = [
  { label: "Просмотры", value: "1,2 млн", color: "#666", svg: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>' },
  { label: "Лайки", value: "1,2 млн", color: "#ef4444", svg: '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>' },
  { label: "Комментарии", value: "1,2 млн", color: "#22c55e", svg: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>' },
  { label: "Репосты", value: "1,2 млн", color: "#3b82f6", svg: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>' },
  { label: "ER", value: "1,2 млн", color: "#f59e0b", svg: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>' },
];
</script>

<template>
  <Transition name="panel">
    <div v-if="publication" class="overlay" @click.self="$emit('close')">
      <div class="panel">
        <button class="panel__close" @click="$emit('close')">✕</button>

        <div class="panel__layout">
          <!-- Левая часть — видео -->
          <div class="panel__left">
            <div class="panel__video">
              <img src="/assets/video-preview.png" alt="" />
              <div class="panel__video-badges">
                <span class="panel__video-badge">📱 Reels</span>
                <span class="panel__video-badge">🔥 X10</span>
              </div>
              <button class="panel__video-play">▶</button>
            </div>

            <div class="panel__date">{{ formatDateTime(publication.created_at) }}</div>

            <div class="panel__bloger">
              <img src="https://i.pravatar.cc/64?img=47" class="panel__bloger-avatar" />
              <div>
                <div class="panel__bloger-name">@blogerich</div>
                <div class="panel__bloger-followers">384.5K</div>
              </div>
            </div>

            <p class="panel__desc">{{ publication.text }} <span class="panel__more">Ещё</span></p>

            <div class="panel__stats">
              <div v-for="s in stats" :key="s.label" class="panel__stat">
                <span class="panel__stat-icon" :style="{ color: s.color }" v-html="s.svg" />
                <span class="panel__stat-label">{{ s.label }}</span>
                <span class="panel__stat-value">{{ s.value }}</span>
              </div>
            </div>
          </div>

          <!-- Правая часть — разбор -->
          <div class="panel__right">
            <div class="panel__label">Тема видео</div>
            <h2 class="panel__title">{{ publication.title }}</h2>

            <div class="panel__meta">
              <span>🎵 Tyga – Pop it off</span>
              <span>Язык: 🇬🇧 Английский</span>
            </div>

            <div class="panel__tags">
              <span v-for="tag in tags" :key="tag.label" class="panel__tag" :class="tag.cls">{{ tag.label }}</span>
            </div>

            <!-- Транскрибация -->
            <section class="section">
              <div class="section__head">
                <h3>Транскрибация</h3>
                <span class="section__action">✨ Переведено</span>
              </div>
              <div class="section__body">
                <p>{{ publication.text }}</p>
                <span class="section__more">Ещё</span>
              </div>
            </section>

            <button class="panel__adapt">✏️ Адаптировать</button>

            <!-- Суть -->
            <section class="section">
              <h3>Суть</h3>
              <div class="section__body">
                <p>Разбор состава/логики: он в человеческих словах переводит состав/механику ("что реально делает Х"), называет 2–3 работающих активных компонента и 2–3 маркетинговых "пустых" обещаний.</p>
              </div>
            </section>

            <!-- Структура -->
            <section class="section">
              <h3>Структура</h3>
              <div class="timeline">
                <div class="timeline__item">
                  <span class="timeline__time">0-3 сек</span>
                  <span class="timeline__dot" />
                  <div><strong>Шок-сравнение</strong><p>Визуальный (Девушка с предметом) + Текст на экране: "Это спасёт вашу зиму"</p></div>
                </div>
                <div class="timeline__item">
                  <span class="timeline__time">3-15 сек</span>
                  <span class="timeline__dot timeline__dot--half" />
                  <div><strong>Сюжет</strong><p>[Герой] показывает проблему → Резкар смена кадра → Решение</p></div>
                </div>
                <div class="timeline__item">
                  <span class="timeline__time">15-120 сек</span>
                  <span class="timeline__dot timeline__dot--full" />
                  <div><strong>Финал / CTA</strong><p>Призыв: "Пиши слово "ССЫЛКА" в комменты"</p></div>
                </div>
              </div>
            </section>

            <!-- Хуки -->
            <div v-for="hook in ['Хук фраза', 'Визуальный хук', 'Текстовый хук']" :key="hook" class="hook">
              <div class="hook__head"><strong>{{ hook }}</strong><span class="hook__copy">📋</span></div>
              <p class="hook__text">Одна из них — пустышка. Угадаешь какая?</p>
            </div>

            <!-- Рабочие приемы -->
            <section class="section">
              <div class="section__head"><h3>Рабочие приемы</h3><span class="hook__copy">📋</span></div>
              <div class="section__body">
                <h4>2. Суть видео</h4>
                <p>Приём: "кому подходит / кому нет" двумя блоками.</p>
                <p>Почему сработало: это формат "диагноз → лечение → решение".</p>
                <h4>3. Монтаж</h4>
                <p>Приём: смена планов каждые 1–2 секунды: лицо → продукт крупно → рука (демо) → снова лицо.</p>
                <p>Почему сработало: вертикалки смотрят на автопилоте.</p>
                <h4>4. Реплики</h4>
                <p>Приём: "триггер доверия" одной фразой: "Я не продаю этот SPF, мне пох, скажу как есть."</p>
                <p>Почему сработало: снимает защиту "мне впаривают".</p>
              </div>
            </section>

            <!-- Воронка -->
            <section class="section">
              <div class="section__head"><h3>Воронка / Маркетинг</h3><span class="hook__copy">📋</span></div>
              <div class="section__body">
                <div v-for="f in ['CTA голос/визуал', 'Тригер', 'Куда ведет', 'Лид-магнит']" :key="f">
                  <h4>{{ f }}</h4>
                  <p>Почему сработало: зритель узнаёт свой баг мгновенно. Это не "мнение", а физический факт в кадре, мозг цепляется.</p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 100; display: flex; justify-content: center; overflow-y: auto; padding: 20px; }

.panel { background: #fff; border-radius: 16px; max-width: 960px; width: 100%; position: relative; margin: auto; }

.panel__close { position: absolute; top: 14px; right: 18px; background: none; border: none; font-size: 18px; color: #bbb; cursor: pointer; z-index: 10; }

.panel__layout { display: flex; }

/* Левая часть */
.panel__left { width: 320px; min-width: 320px; padding: 20px; border-right: 1px solid #f0f0f0; }

.panel__video { position: relative; border-radius: 12px; overflow: hidden; aspect-ratio: 9/14; background: #111; }
.panel__video img { width: 100%; height: 100%; object-fit: cover; }
.panel__video-badges { position: absolute; top: 8px; left: 8px; display: flex; flex-direction: column; gap: 4px; }
.panel__video-badge { padding: 3px 7px; border-radius: 6px; font-size: 10px; font-weight: 600; color: #fff; background: rgba(255,255,255,0.18); backdrop-filter: blur(6px); }
.panel__video-play { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 40px; height: 40px; border-radius: 50%; border: none; background: rgba(255,255,255,0.25); color: #fff; font-size: 16px; cursor: pointer; }

.panel__date { font-size: 11px; color: #aaa; margin-top: 10px; }

.panel__bloger { display: flex; align-items: center; gap: 8px; margin-top: 10px; }
.panel__bloger-avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }
.panel__bloger-name { font-size: 13px; font-weight: 600; }
.panel__bloger-followers { font-size: 11px; color: #999; }

.panel__desc { font-size: 12px; color: #444; margin-top: 10px; line-height: 1.5; }
.panel__more { color: var(--color-accent); cursor: pointer; font-weight: 500; }

.panel__stats { margin-top: 14px; }
.panel__stat { display: flex; align-items: center; gap: 8px; padding: 6px 0; border-bottom: 1px solid #f5f5f5; font-size: 13px; }
.panel__stat-icon { width: 20px; text-align: center; }
.panel__stat-label { flex: 1; color: #777; }
.panel__stat-value { font-weight: 600; }

/* Правая часть */
.panel__right { flex: 1; padding: 24px 28px 32px; max-height: 90vh; overflow-y: auto; }

.panel__label { font-size: 11px; color: #aaa; text-transform: uppercase; letter-spacing: 0.4px; }
.panel__title { font-size: 20px; font-weight: 700; margin-top: 3px; line-height: 1.3; }
.panel__meta { display: flex; gap: 14px; margin-top: 8px; font-size: 12px; color: #888; }
.panel__tags { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
.panel__tag { padding: 3px 10px; border-radius: 14px; font-size: 11px; font-weight: 500; border: 1px solid; }
.tag--orange { color: #ea580c; background: #fff7ed; border-color: #fed7aa; }
.tag--green { color: #16a34a; background: #f0fdf4; border-color: #bbf7d0; }
.tag--indigo { color: #4f46e5; background: #eef2ff; border-color: #c7d2fe; }

/* Секции */
.section { margin-top: 22px; }
.section__head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.section h3 { font-size: 15px; font-weight: 700; }
.section__action { font-size: 12px; color: var(--color-accent); font-weight: 500; }
.section__body { background: #f8f8fa; border-radius: 10px; padding: 14px; font-size: 13px; line-height: 1.7; color: #555; }
.section__body p { margin-bottom: 5px; }
.section__body h4 { font-size: 13.5px; font-weight: 600; color: #333; margin: 12px 0 4px; }
.section__body h4:first-child { margin-top: 0; }
.section__more { color: var(--color-accent); cursor: pointer; font-weight: 500; }

.panel__adapt { margin-top: 16px; padding: 10px 22px; border: none; border-radius: 10px; background: var(--color-accent); color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; font-family: inherit; }

/* Таймлайн */
.timeline { margin-top: 8px; padding-left: 70px; }
.timeline__item { display: flex; gap: 14px; padding: 10px 0; border-left: 2px solid #e5e5e5; padding-left: 18px; position: relative; font-size: 13px; }
.timeline__time { position: absolute; left: -68px; font-size: 11px; color: #aaa; white-space: nowrap; top: 12px; }
.timeline__dot { position: absolute; left: -7px; top: 13px; width: 11px; height: 11px; border-radius: 50%; border: 2px solid #d0d0d0; background: #fff; }
.timeline__dot--half { border-color: var(--color-accent); }
.timeline__dot--full { border-color: var(--color-accent); background: var(--color-accent); }
.timeline__item strong { display: block; margin-bottom: 2px; }
.timeline__item p { color: #777; font-size: 12px; }

/* Хуки */
.hook { margin-top: 18px; padding-bottom: 14px; border-bottom: 1px solid #f0f0f0; }
.hook__head { display: flex; justify-content: space-between; align-items: center; }
.hook__copy { cursor: pointer; opacity: 0.4; }
.hook__copy:hover { opacity: 1; }
.hook__text { font-size: 13px; color: #777; margin-top: 4px; }

/* Анимация */
.panel-enter-active, .panel-leave-active { transition: opacity 0.25s ease; }
.panel-enter-active .panel, .panel-leave-active .panel { transition: transform 0.25s ease; }
.panel-enter-from, .panel-leave-to { opacity: 0; }
.panel-enter-from .panel { transform: translateY(12px); }

@media (max-width: 768px) {
  .panel__layout { flex-direction: column; }
  .panel__left { width: 100%; min-width: auto; border-right: none; border-bottom: 1px solid #f0f0f0; }
}
</style>