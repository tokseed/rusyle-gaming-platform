<template>
  <div class="admin-container">
    <div class="admin-header">
      <h1>⚙️ Панель администратора</h1>
      <p class="subtitle">Управление платформой RuSyle</p>
    </div>

    <!-- Навигация по вкладкам -->
    <div class="admin-tabs">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        :class="{ active: activeTab === tab }"
        class="tab-btn"
      >
        {{ tabLabels[tab] }}
      </button>
    </div>

    <!-- Содержимое вкладок -->
    <div class="admin-content">
      <!-- Статистика -->
      <div v-if="activeTab === 'stats'" class="section">
        <h2>📊 Статистика</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-value">{{ stats.users }}</span>
            <span class="stat-label">Пользователей</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.events }}</span>
            <span class="stat-label">События</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.reviews }}</span>
            <span class="stat-label">Отзывов</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.activeUsers }}</span>
            <span class="stat-label">Активных сегодня</span>
          </div>
        </div>
      </div>

      <!-- Пользователи -->
      <div v-if="activeTab === 'users'" class="section">
        <h2>👥 Управление пользователями</h2>
        <div class="users-list">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Email</th>
                <th>Имя</th>
                <th>Роль</th>
                <th>Статус</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>#{{ user.id }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.full_name }}</td>
                <td>
                  <span class="badge" :class="user.role">
                    {{ user.role === 'admin' ? '👑 Admin' : '👤 User' }}
                  </span>
                </td>
                <td>
                  <span class="badge" :class="user.is_active ? 'active' : 'inactive'">
                    {{ user.is_active ? '✅ Active' : '❌ Blocked' }}
                  </span>
                </td>
                <td>
                  <button @click="toggleUserStatus(user)" class="action-btn">
                    {{ user.is_active ? 'Заблокировать' : 'Разблокировать' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- События -->
      <div v-if="activeTab === 'events'" class="section">
        <h2>📅 Управление событиями</h2>
        <button @click="showAddEvent = true" class="btn-add">
          ➕ Добавить событие
        </button>

        <div class="events-list">
          <div v-for="event in events" :key="event.id" class="event-item">
            <div class="event-info">
              <h3>{{ event.title }}</h3>
              <p>{{ event.developer }} • {{ event.status }}</p>
            </div>
            <div class="event-actions">
              <button @click="editEvent(event)" class="action-btn">✏️ Редактировать</button>
              <button @click="deleteEvent(event.id)" class="action-btn delete">🗑️ Удалить</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Экспорт -->
      <div v-if="activeTab === 'export'" class="section">
        <h2>📥 Экспорт данных</h2>
        <p class="description">
          Загрузите данные в формате JSON для анализа или резервного копирования
        </p>

        <div class="export-buttons">
          <button @click="exportData('users')" class="export-btn">
            📄 Экспортировать пользователей
          </button>
          <button @click="exportData('events')" class="export-btn">
            📄 Экспортировать события
          </button>
          <button @click="exportData('all')" class="export-btn primary">
            📦 Экспортировать всё
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth.js'

const authStore = useAuthStore()

// Проверка админа
if (!authStore.isAdmin) {
  alert('⛔ Доступ запрещен')
  window.location.href = '/'
}

const activeTab = ref('stats')
const showAddEvent = ref(false)

const tabLabels = {
  stats: '📊 Статистика',
  users: '👥 Пользователи',
  events: '📅 События',
  export: '📥 Экспорт'
}

const tabs = Object.keys(tabLabels)

// Статистика
const stats = ref({
  users: 156,
  events: 42,
  reviews: 287,
  activeUsers: 23
})

// Пользователи (мок данные)
const users = ref([
  { id: 1, email: 'test@example.com', full_name: 'Тест Юзер', role: 'user', is_active: true },
  { id: 2, email: 'admin@example.com', full_name: 'Администратор', role: 'admin', is_active: true }
])

// События (мок данные)
const events = ref([
  {
    id: 1,
    title: 'Cyberpunk 2077',
    developer: 'CD Projekt Red',
    status: 'released'
  },
  {
    id: 2,
    title: 'The Witcher 4',
    developer: 'CD Projekt Red',
    status: 'upcoming'
  }
])

const toggleUserStatus = (user) => {
  user.is_active = !user.is_active
  alert(user.is_active ? '✅ Пользователь разблокирован' : '❌ Пользователь заблокирован')
}

const editEvent = (event) => {
  alert(`✏️ Редактирование события: ${event.title}`)
}

const deleteEvent = (eventId) => {
  if (confirm('Вы уверены?')) {
    events.value = events.value.filter(e => e.id !== eventId)
    alert('✅ Событие удалено')
  }
}

const exportData = (type) => {
  let data = {}

  if (type === 'users' || type === 'all') {
    data.users = users.value
  }
  if (type === 'events' || type === 'all') {
    data.events = events.value
  }

  const json = JSON.stringify(data, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `rusyle-export-${type}-${new Date().toISOString().split('T')[0]}.json`
  a.click()
}
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.admin-header {
  text-align: center;
  margin-bottom: 3rem;
}

.admin-header h1 {
  font-size: 2.5rem;
  color: #00d4ff;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #b0b0b0;
}

.admin-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #333;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background: transparent;
  color: #b0b0b0;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.tab-btn:hover {
  color: #e0e0e0;
}

.tab-btn.active {
  color: #00d4ff;
  border-bottom-color: #00d4ff;
}

.admin-content {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 0.75rem;
  padding: 2rem;
}

.section h2 {
  font-size: 1.5rem;
  color: #e0e0e0;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #333;
  padding-bottom: 0.75rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: #0f0f0f;
  border: 1px solid #333;
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  color: #00d4ff;
  margin-bottom: 0.5rem;
}

.stat-label {
  display: block;
  color: #b0b0b0;
  font-size: 0.9rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}

.data-table th {
  background: #0f0f0f;
  color: #b0b0b0;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 1px solid #333;
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #333;
  color: #e0e0e0;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  background: #333;
  color: #b0b0b0;
}

.badge.admin {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.badge.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.badge.inactive {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.action-btn {
  padding: 0.4rem 0.8rem;
  background: #333;
  color: #b0b0b0;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: #444;
  color: #e0e0e0;
}

.action-btn.delete {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.action-btn.delete:hover {
  background: rgba(255, 107, 107, 0.3);
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-item {
  background: #0f0f0f;
  border: 1px solid #333;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-info h3 {
  margin: 0 0 0.25rem 0;
  color: #e0e0e0;
}

.event-info p {
  margin: 0;
  color: #707070;
  font-size: 0.9rem;
}

.event-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-add {
  padding: 0.75rem 1.5rem;
  background: #00d4ff;
  color: #0f0f0f;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: all 0.3s;
}

.btn-add:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}

.description {
  color: #b0b0b0;
  margin-bottom: 2rem;
}

.export-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.export-btn {
  padding: 1rem;
  background: #333;
  color: #e0e0e0;
  border: 1px solid #555;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.export-btn:hover {
  background: #444;
  border-color: #00d4ff;
}

.export-btn.primary {
  background: #00d4ff;
  color: #0f0f0f;
  border-color: #00d4ff;
}

.export-btn.primary:hover {
  background: #00b8cc;
}

@media (max-width: 768px) {
  .event-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .event-actions {
    width: 100%;
  }

  .action-btn {
    flex: 1;
  }

  .data-table {
    font-size: 0.9rem;
  }

  .data-table th,
  .data-table td {
    padding: 0.5rem;
  }
}
</style>
