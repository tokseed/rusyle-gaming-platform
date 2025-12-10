<template>
  <div class="event-detail-container">
    <!-- Назад -->
    <router-link to="/events" class="btn-back">← Вернуться к событиям</router-link>

    <!-- Загрузка -->
    <div v-if="loading" class="loading-state">
      ⏳ Загружаем детали события...
    </div>

    <!-- Содержимое -->
    <div v-if="!loading && event" class="event-detail">
      <!-- Заголовок -->
      <div class="hero-section">
        <img
          v-if="event.image_url"
          :src="event.image_url"
          :alt="event.title"
          class="hero-image"
        />
        <div v-else class="hero-placeholder">🎮 Изображение события</div>

        <div class="hero-overlay">
          <h1>{{ event.title }}</h1>
          <p class="developer">{{ event.developer }}</p>
          <span v-if="event.status" class="status-badge" :class="event.status">
            {{ statusLabel }}
          </span>
        </div>
      </div>

      <!-- Основная информация -->
      <div class="content-grid">
        <!-- Основной контент -->
        <div class="main-content">
          <!-- Описание -->
          <section class="section">
            <h2>📖 Описание</h2>
            <p>{{ event.description }}</p>
          </section>

          <!-- Характеристики -->
          <section class="section">
            <h2>⚙️ Характеристики</h2>
            <div class="specs-grid">
              <div class="spec">
                <span class="spec-label">Жанр:</span>
                <span class="spec-value">{{ event.genre }}</span>
              </div>
              <div class="spec">
                <span class="spec-label">Платформы:</span>
                <span class="spec-value">{{ event.platform }}</span>
              </div>
              <div class="spec">
                <span class="spec-label">Дата выпуска:</span>
                <span class="spec-value">{{ formatDate(event.release_date) }}</span>
              </div>
              <div class="spec">
                <span class="spec-label">Рейтинг:</span>
                <span class="spec-value">⭐ {{ event.rating }}/10</span>
              </div>
            </div>
          </section>

          <!-- Ссылки -->
          <section v-if="event.website || event.steam_id" class="section">
            <h2>🔗 Ссылки</h2>
            <div class="links">
              <a
                v-if="event.website"
                :href="event.website"
                target="_blank"
                rel="noopener noreferrer"
                class="link-btn"
              >
                🌐 Официальный сайт
              </a>
              <a
                v-if="event.steam_id"
                :href="`https://steamcommunity.com/app/${event.steam_id}`"
                target="_blank"
                rel="noopener noreferrer"
                class="link-btn"
              >
                🎮 Steam
              </a>
            </div>
          </section>
        </div>

        <!-- Боковая панель -->
        <aside class="sidebar">
          <!-- Карточка события -->
          <div class="info-card">
            <h3>ℹ️ Информация</h3>
            <div class="info-item">
              <span class="label">Разработчик:</span>
              <span class="value">{{ event.developer }}</span>
            </div>
            <div class="info-item">
              <span class="label">Статус:</span>
              <span class="value">{{ statusLabel }}</span>
            </div>
            <div class="info-item">
              <span class="label">Рейтинг:</span>
              <span class="value">{{ event.rating }}/10</span>
            </div>
          </div>

          <!-- Действия -->
          <div class="actions">
            <button @click="toggleParticipate" class="btn-primary">
              {{ isParticipating ? '✅ Вы участвуете' : '➕ Присоединиться' }}
            </button>
            <button class="btn-secondary">
              💬 Написать отзыв
            </button>
          </div>
        </aside>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-if="!loading && error" class="error-state">
      <p>⚠️ {{ error }}</p>
      <router-link to="/events" class="btn-primary">
        Вернуться к событиям
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventsStore } from '@/store/events.js'

const route = useRoute()
const router = useRouter()
const eventsStore = useEventsStore()

const loading = ref(false)
const error = ref(null)
const isParticipating = ref(false)

const event = computed(() => eventsStore.currentEvent)

const statusLabel = computed(() => {
  const statusMap = {
    'released': '📦 Выпущено',
    'early_access': '🔨 Early Access',
    'upcoming': '🎯 Скоро',
    'active': '🔥 Активное',
    'past': '📜 Прошедшее'
  }
  return statusMap[event.value?.status] || event.value?.status
})

const formatDate = (dateString) => {
  if (!dateString) return 'Дата не указана'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const toggleParticipate = async () => {
  try {
    if (isParticipating.value) {
      await eventsStore.cancelParticipation(event.value.id)
    } else {
      await eventsStore.participate(event.value.id)
    }
    isParticipating.value = !isParticipating.value
  } catch (err) {
    error.value = 'Ошибка при изменении статуса участия'
  }
}

onMounted(async () => {
  const eventId = route.params.id
  loading.value = true
  error.value = null

  try {
    await eventsStore.fetchEventById(eventId)
    // Проверяем, участвует ли пользователь
    isParticipating.value = event.value?.is_participant || false
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о событии'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.event-detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.btn-back {
  display: inline-block;
  margin-bottom: 2rem;
  color: #00d4ff;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-back:hover {
  transform: translateX(-4px);
}

.loading-state,
.error-state {
  padding: 3rem;
  text-align: center;
  background: #1a1a1a;
  border-radius: 0.75rem;
  border: 1px solid #333;
}

.loading-state {
  color: #00d4ff;
  font-size: 1.2rem;
}

.error-state {
  color: #ff6b6b;
}

.error-state p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.event-detail {
  background: #0f0f0f;
  border-radius: 1rem;
  overflow: hidden;
}

.hero-section {
  position: relative;
  height: 400px;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 212, 255, 0.05) 100%);
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #333;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 3rem 2rem;
  background: linear-gradient(180deg, transparent 0%, rgba(15, 15, 15, 0.9) 100%);
}

.hero-overlay h1 {
  font-size: 2.5rem;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.developer {
  font-size: 1.2rem;
  color: #00d4ff;
  margin-bottom: 1rem;
}

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 600;
  background: #00d4ff;
  color: #0f0f0f;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  padding: 2rem;
}

.section {
  margin-bottom: 2rem;
}

.section h2 {
  font-size: 1.5rem;
  color: #e0e0e0;
  margin-bottom: 1rem;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
}

.section p {
  color: #b0b0b0;
  line-height: 1.6;
}

.specs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.spec {
  background: #1a1a1a;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #333;
}

.spec-label {
  display: block;
  color: #707070;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.spec-value {
  display: block;
  color: #e0e0e0;
  font-weight: 600;
}

.links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.link-btn {
  padding: 0.75rem 1.5rem;
  background: #00d4ff;
  color: #0f0f0f;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.link-btn:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.info-card h3 {
  color: #00d4ff;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #333;
}

.info-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.label {
  color: #707070;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.value {
  color: #e0e0e0;
  font-weight: 600;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background: #00d4ff;
  color: #0f0f0f;
}

.btn-primary:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #333;
  color: #e0e0e0;
}

.btn-secondary:hover {
  background: #444;
}

@media (max-width: 768px) {
  .event-detail-container {
    padding: 1rem;
  }

  .hero-section {
    height: 250px;
  }

  .hero-overlay {
    padding: 2rem 1rem;
  }

  .hero-overlay h1 {
    font-size: 1.8rem;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .specs-grid {
    grid-template-columns: 1fr;
  }
}
</style>
