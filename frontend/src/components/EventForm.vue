<template>
  <div class="event-form-wrapper">
    <div class="form-header">
      <h2>{{ isEditing ? '✏️ Редактирование события' : '➕ Создание события' }}</h2>
      <p class="form-subtitle">Заполните все поля для {{ isEditing ? 'обновления' : 'создания' }} события</p>
    </div>

    <form @submit.prevent="handleSubmit" class="event-form">
      <!-- Название -->
      <div class="form-group">
        <label for="title">Название события *</label>
        <input
          v-model="form.title"
          id="title"
          type="text"
          placeholder="Введите название события"
          required
        />
      </div>

      <!-- Разработчик -->
      <div class="form-group">
        <label for="developer">Разработчик *</label>
        <input
          v-model="form.developer"
          id="developer"
          type="text"
          placeholder="Название компании-разработчика"
          required
        />
      </div>

      <!-- Жанр -->
      <div class="form-group">
        <label for="genre">Жанр *</label>
        <input
          v-model="form.genre"
          id="genre"
          type="text"
          placeholder="Например: Экшен, RPG, Стратегия"
          required
        />
      </div>

      <!-- Платформы -->
      <div class="form-group">
        <label for="platform">Платформы *</label>
        <textarea
          v-model="form.platform"
          id="platform"
          placeholder="PC, PS5, Xbox, Nintendo Switch и т.д."
          rows="2"
          required
        ></textarea>
      </div>

      <!-- Дата выпуска -->
      <div class="form-group">
        <label for="release_date">Дата выпуска/события *</label>
        <input
          v-model="form.release_date"
          id="release_date"
          type="date"
          required
        />
      </div>

      <!-- Описание -->
      <div class="form-group">
        <label for="description">Описание *</label>
        <textarea
          v-model="form.description"
          id="description"
          placeholder="Подробное описание события"
          rows="4"
          required
        ></textarea>
      </div>

      <!-- Рейтинг -->
      <div class="form-group">
        <label for="rating">Рейтинг (0-10)</label>
        <input
          v-model.number="form.rating"
          id="rating"
          type="number"
          min="0"
          max="10"
          step="0.1"
          placeholder="8.5"
        />
      </div>

      <!-- Изображение (URL) -->
      <div class="form-group">
        <label for="image_url">URL изображения</label>
        <input
          v-model="form.image_url"
          id="image_url"
          type="url"
          placeholder="https://example.com/image.jpg"
        />
        <small v-if="form.image_url" class="image-preview">
          Превью: <img :src="form.image_url" alt="Preview" />
        </small>
      </div>

      <!-- Статус -->
      <div class="form-group">
        <label for="status">Статус *</label>
        <select v-model="form.status" id="status" required>
          <option value="">Выберите статус</option>
          <option value="released">📦 Выпущено</option>
          <option value="early_access">🔨 Early Access</option>
          <option value="upcoming">🎯 Скоро</option>
          <option value="active">🔥 Активное</option>
          <option value="past">📜 Прошедшее</option>
        </select>
      </div>

      <!-- Вебсайт -->
      <div class="form-group">
        <label for="website">Официальный вебсайт</label>
        <input
          v-model="form.website"
          id="website"
          type="url"
          placeholder="https://example.com"
        />
      </div>

      <!-- Steam ID -->
      <div class="form-group">
        <label for="steam_id">Steam ID</label>
        <input
          v-model="form.steam_id"
          id="steam_id"
          type="text"
          placeholder="Например: 668580"
        />
      </div>

      <!-- Ошибки -->
      <div v-if="error" class="error-message">
        ⚠️ {{ error }}
      </div>

      <!-- Кнопки -->
      <div class="form-actions">
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Загрузка...' : (isEditing ? 'Сохранить изменения' : 'Создать событие') }}
        </button>
        <button type="button" @click="$emit('cancel')" class="btn-secondary">
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  event: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const error = ref(null)

const form = ref({
  title: '',
  developer: '',
  genre: '',
  platform: '',
  release_date: '',
  description: '',
  rating: 0,
  image_url: '',
  status: '',
  website: '',
  steam_id: ''
})

const isEditing = computed(() => !!props.event)

// Заполни форму при редактировании
watch(
  () => props.event,
  (newEvent) => {
    if (newEvent) {
      form.value = { ...newEvent }
    }
  },
  { immediate: true }
)

const handleSubmit = () => {
  error.value = null

  // Валидация
  if (!form.value.title) {
    error.value = 'Название события обязательно'
    return
  }
  if (!form.value.developer) {
    error.value = 'Разработчик обязателен'
    return
  }
  if (!form.value.release_date) {
    error.value = 'Дата события обязательна'
    return
  }

  emit('submit', form.value)
}
</script>

<style scoped>
.event-form-wrapper {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 0.75rem;
  padding: 2rem;
}

.form-header {
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.5rem;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.event-form {
  display: grid;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #b0b0b0;
  font-size: 0.95rem;
}

input,
select,
textarea {
  padding: 0.75rem;
  background: #0f0f0f;
  border: 1px solid #333;
  border-radius: 0.5rem;
  color: #e0e0e0;
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.image-preview {
  display: block;
  margin-top: 0.75rem;
  color: #b0b0b0;
  font-size: 0.85rem;
}

.image-preview img {
  max-width: 200px;
  max-height: 150px;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  border: 1px solid #333;
}

.error-message {
  padding: 1rem;
  background: rgba(255, 107, 107, 0.1);
  border-left: 3px solid #ff6b6b;
  color: #ff6b6b;
  border-radius: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  flex: 1;
}

.btn-primary {
  background: #00d4ff;
  color: #0f0f0f;
}

.btn-primary:hover:not(:disabled) {
  background: #00b8cc;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #333;
  color: #e0e0e0;
}

.btn-secondary:hover {
  background: #444;
}

@media (max-width: 768px) {
  .event-form-wrapper {
    padding: 1.5rem;
  }

  .form-header h2 {
    font-size: 1.2rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    flex: auto;
  }
}
</style>
