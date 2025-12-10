<template>
  <div class="events-container">
    <!-- Header -->
    <div class="events-header">
      <div class="header-top">
        <h1>🎮 Афиша событий</h1>
        <button @click="logout" class="btn-logout">Выйти</button>
      </div>
      
      <div v-if="currentUser" class="user-info">
        👤 {{ currentUser.full_name }}
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="🔍 Поиск событий..."
        class="search-input"
      />
    </div>

    <!-- Список событий -->
    <div class="events-list">
      <div v-if="loading" class="loading">
        ⏳ Загрузка...
      </div>

      <div v-else-if="filteredEvents.length === 0" class="no-events">
        📭 События не найдены
      </div>

      <div v-else class="events-grid">
        <div 
          v-for="event in filteredEvents" 
          :key="event.id" 
          class="event-card"
          @click="selectEvent(event)"
        >
          <div class="event-header">
            <h3>{{ event.title }}</h3>
            <span class="status" :class="event.status">{{ event.status }}</span>
          </div>
          
          <div class="event-details">
            <p><strong>Разработчик:</strong> {{ event.developer }}</p>
            <p><strong>Жанр:</strong> {{ event.genre }}</p>
          </div>

          <div class="event-footer">
            <button @click.stop="participateEvent(event.id)" class="btn-participate">
              ✨ Участвовать
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно события -->
    <div v-if="selectedEvent" class="modal-overlay" @click="selectedEvent = null">
      <div class="modal" @click.stop>
        <button class="modal-close" @click="selectedEvent = null">✕</button>
        
        <h2>{{ selectedEvent.title }}</h2>
        
        <div class="modal-details">
          <p><strong>Разработчик:</strong> {{ selectedEvent.developer }}</p>
          <p><strong>Жанр:</strong> {{ selectedEvent.genre }}</p>
          <p><strong>Статус:</strong> {{ selectedEvent.status }}</p>
        </div>

        <div class="modal-actions">
          <button @click="participateEvent(selectedEvent.id)" class="btn-primary">
            ✨ Участвовать
          </button>
          <button @click="selectedEvent = null" class="btn-secondary">
            Закрыть
          </button>
        </div>
      </div>
    </div>

    <!-- Уведомление -->
    <div v-if="notification" class="notification" :class="notification.type">
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const events = ref([])
const searchQuery = ref('')
const loading = ref(false)
const selectedEvent = ref(null)
const currentUser = ref(null)
const notification = ref(null)

const API_URL = 'http://127.0.0.1:5000/api'

// Фильтрованные события
const filteredEvents = computed(() => {
  return events.value.filter(event => 
    event.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    event.developer.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Загружаем события при открытии страницы
const loadEvents = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_URL}/events`)
    const data = await response.json()
    events.value = data
  } catch (err) {
    showNotification('Ошибка загрузки событий', 'error')
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Участие в событии
const participateEvent = async (eventId) => {
  const token = localStorage.getItem('token')
  
  if (!token) {
    showNotification('Требуется авторизация', 'error')
    router.push('/auth')
    return
  }

  try {
    const response = await fetch(`${API_URL}/events/${eventId}/participate`, {
      method: 'POST',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      showNotification('✅ Вы присоединились к событию!', 'success')
      selectedEvent.value = null
    } else {
      showNotification('Ошибка при присоединении', 'error')
    }
  } catch (err) {
    showNotification('Ошибка подключения', 'error')
    console.error(err)
  }
}

// Выход
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/auth')
}

// Выбор события
const selectEvent = (event) => {
  selectedEvent.value = event
}

// Уведомление
const showNotification = (message, type = 'success') => {
  notification.value = { message, type }
  setTimeout(() => {
    notification.value = null
  }, 3000)
}

// При загрузке компонента
onMounted(() => {
  const user = localStorage.getItem('user')
  const token = localStorage.getItem('token')

  // Если нет токена, перенаправляем на авторизацию
  if (!token) {
    router.push('/auth')
    return
  }

  currentUser.value = user ? JSON.parse(user) : null
  loadEvents()
})
</script>

<style scoped>
.events-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20px;
}

.events-header {
  max-width: 1200px;
  margin: 0 auto 30px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.events-header h1 {
  color: #00d4ff;
  font-size: 32px;
  margin: 0;
}

.btn-logout {
  padding: 10px 20px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-logout:hover {
  background: #ff5252;
  transform: translateY(-2px);
}

.user-info {
  color: #a0a0a0;
  font-size: 14px;
}

.filters {
  max-width: 1200px;
  margin: 0 auto 30px;
  display: flex;
  gap: 15px;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #333;
  border-radius: 6px;
  background: #0f3460;
  color: #e0e0e0;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

.events-list {
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .no-events {
  text-align: center;
  color: #a0a0a0;
  padding: 40px 20px;
  font-size: 18px;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.event-card {
  background: #0f3460;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.event-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
  transform: translateY(-5px);
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
}

.event-header h3 {
  color: #e0e0e0;
  margin: 0;
  font-size: 18px;
  flex: 1;
}

.status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status.upcoming {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status.released {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
}

.event-details {
  color: #a0a0a0;
  font-size: 14px;
}

.event-details p {
  margin: 5px 0;
}

.event-details strong {
  color: #e0e0e0;
}

.event-footer {
  display: flex;
  gap: 10px;
}

.btn-participate {
  flex: 1;
  padding: 10px 15px;
  background: #00d4ff;
  color: #0f3460;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-participate:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}

/* МОДАЛЬНОЕ ОКНО */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #0f3460;
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 30px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  color: #a0a0a0;
  font-size: 24px;
  cursor: pointer;
  transition: color 0.3s;
}

.modal-close:hover {
  color: #00d4ff;
}

.modal h2 {
  color: #00d4ff;
  margin-top: 0;
}

.modal-details {
  color: #a0a0a0;
  margin-bottom: 20px;
}

.modal-details p {
  margin: 10px 0;
}

.modal-details strong {
  color: #e0e0e0;
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.btn-primary {
  flex: 1;
  padding: 12px 20px;
  background: #00d4ff;
  color: #0f3460;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}

.btn-secondary {
  flex: 1;
  padding: 12px 20px;
  background: #333;
  color: #a0a0a0;
  border: 1px solid #555;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: #444;
  color: #e0e0e0;
}

/* УВЕДОМЛЕНИЕ */
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 6px;
  font-weight: 600;
  z-index: 2000;
  animation: slideIn 0.3s ease-out;
}

.notification.success {
  background: #4caf50;
  color: white;
}

.notification.error {
  background: #ff6b6b;
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .events-grid {
    grid-template-columns: 1fr;
  }
}
</style>
