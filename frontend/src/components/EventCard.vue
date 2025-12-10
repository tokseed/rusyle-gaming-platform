<template>
  <div class="event-card">
    <div class="event-image">
      <img
        :src="event.image_url || 'https://via.placeholder.com/300x200?text=Game+Event'"
        :alt="event.title"
      />
      <span v-if="event.status" class="event-status" :class="event.status">
        {{ statusLabel }}
      </span>
    </div>

    <div class="event-body">
      <h3 class="event-title">{{ event.title }}</h3>
      <p class="event-developer">{{ event.developer }}</p>

      <div class="event-meta">
        <span class="genre">{{ event.genre }}</span>
        <span class="rating">⭐ {{ event.rating }}</span>
      </div>

      <p class="event-description">{{ truncateDescription(event.description) }}</p>

      <div class="event-footer">
        <span class="event-date">{{ formatDate(event.release_date) }}</span>
        <button @click="$emit('view-details')" class="btn-details">
          Подробнее →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  event: {
    type: Object,
    required: true
  }
})

defineEmits(['view-details'])

const statusLabel = computed(() => {
  const statusMap = {
    'released': '📦 Выпущено',
    'early_access': '🔨 Early Access',
    'upcoming': '🎯 Скоро',
    'active': '🔥 Активное',
    'past': '📜 Прошедшее'
  }
  return statusMap[props.event.status] || props.event.status
})

const formatDate = (dateString) => {
  if (!dateString) return 'Дата не указана'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const truncateDescription = (text) => {
  if (!text) return ''
  return text.length > 120 ? text.substring(0, 120) + '...' : text
}
</script>

<style scoped>
.event-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.event-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 8px 25px rgba(0, 212, 255, 0.15);
  transform: translateY(-4px);
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
  transition: transform 0.3s ease;
}

.event-card:hover .event-image img {
  transform: scale(1.08);
}

.event-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 0.4rem 0.8rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  background: #00d4ff;
  color: #0f0f0f;
}

.event-status.released {
  background: #4caf50;
  color: white;
}

.event-status.early_access {
  background: #ff9800;
  color: white;
}

.event-status.upcoming {
  background: #2196f3;
  color: white;
}

.event-status.active {
  background: #ff5722;
  color: white;
}

.event-status.past {
  background: #757575;
  color: white;
}

.event-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.event-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 0.4rem;
  line-height: 1.3;
}

.event-developer {
  color: #00d4ff;
  font-size: 0.9rem;
  margin-bottom: 0.8rem;
  font-weight: 500;
}

.event-meta {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.genre {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  padding: 0.3rem 0.6rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.rating {
  color: #ffc107;
  font-weight: 600;
  font-size: 0.9rem;
}

.event-description {
  color: #909090;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
  flex-grow: 1;
}

.event-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.event-date {
  color: #707070;
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
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-details:hover {
  background: #00b8cc;
  transform: translateX(2px);
}

.btn-details:active {
  transform: translateX(0);
}

@media (max-width: 768px) {
  .event-card {
    margin-bottom: 1rem;
  }

  .event-title {
    font-size: 1.1rem;
  }

  .event-meta {
    gap: 0.5rem;
  }
}
</style>
