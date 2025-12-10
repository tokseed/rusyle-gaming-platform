<template>
  <div class="events-container">
    <h1>🎮 События Российской Игровой Индустрии</h1>

    <!-- Вкладки -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        :class="['tab-btn', { active: activeTab === tab }]"
      >
        {{ tabLabels[tab] }}
      </button>
    </div>

    <!-- Загрузка -->
    <div v-if="eventsStore.loading" class="loading">
      Загрузка событий...
    </div>

    <!-- Ошибка -->
    <div v-if="eventsStore.error" class="error">
      {{ eventsStore.error }}
    </div>

    <!-- События -->
    <div v-else class="events-grid">
      <div
        v-if="filteredEvents.length === 0"
        class="no-events"
      >
        Нет событий в этой категории
      </div>

      <div
        v-for="event in filteredEvents"
        :key="event.id"
        class="event-card"
      >
        <div class="event-image">
          <img
            :src="event.image_url || 'https://via.placeholder.com/300x200?text=No+Image'"
            :alt="event.title"
          />
          <span class="event-status">{{ event.status }}</span>
        </div>

        <div class="event-info">
          <h3>{{ event.title }}</h3>
          <p class="developer">{{ event.developer }}</p>
          <p class="description">{{ event.description }}</p>

          <div class="event-meta">
            <span class="genre">{{ event.genre }}</span>
            <span class="rating">⭐ {{ event.rating }}</span>
          </div>

          <div class="event-footer">
            <span class="date">{{ formatDate(event.release_date) }}</span>
            <button
              @click="goToDetail(event.id)"
              class="btn-details"
            >
              Подробнее
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '@/store/events.js'

const router = useRouter()
const eventsStore = useEventsStore()

const activeTab = ref('my')
const tabs = ['my', 'active', 'past']
const tabLabels = {
  my: '🎯 Мои события',
  active: '🔥 Активные события',
  past: '📜 Прошедшие события'
}

const filteredEvents = computed(() => {
  switch (activeTab.value) {
    case 'my':
      return eventsStore.myEvents
    case 'active':
      return eventsStore.activeEvents
    case 'past':
      return eventsStore.pastEvents
    default:
      return eventsStore.events
  }
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const goToDetail = (eventId) => {
  router.push(`/events/${eventId}`)
}

onMounted(async () => {
  await eventsStore.fetchEvents()
})
</script>

<style scoped>
.events-container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #00d4ff;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #333;
}

.tab-btn {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: #00d4ff;
}

.tab-btn.active {
  color: #00d4ff;
  border-bottom-color: #00d4ff;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #b0b0b0;
}

.error {
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 0.5rem;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.no-events {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3rem;
  color: #b0b0b0;
  font-size: 1.1rem;
}

.event-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.event-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 8px 25px rgba(0, 212, 255, 0.15);
}

.event-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #0f0f0f;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.event-card:hover .event-image img {
  transform: scale(1.05);
}

.event-status {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #00d4ff;
  color: #0f0f0f;
  padding: 0.4rem 0.8rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.event-info {
  padding: 1.5rem;
}

.event-info h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #e0e0e0;
}

.developer {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.description {
  color: #909090;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.event-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.genre {
  background: #00d4ff;
  color: #0f0f0f;
  padding: 0.3rem 0.6rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.rating {
  color: #ffc107;
  font-weight: 600;
}

.event-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.date {
  color: #909090;
  font-size: 0.85rem;
}

.btn-details {
  background: #00d4ff;
  color: #0f0f0f;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-details:hover {
  background: #00b8cc;
}

@media (max-width: 768px) {
  .events-grid {
    grid-template-columns: 1fr;
  }

  .tabs {
    overflow-x: auto;
    gap: 0;
  }

  .tab-btn {
    white-space: nowrap;
    padding: 0.75rem 1rem;
  }
}
</style>
