<template>
  <div class="reset-container">
    <div class="reset-card">
      <h1>🔐 Новый пароль</h1>
      <p class="subtitle">Установите новый пароль для аккаунта</p>

      <form @submit.prevent="handleSubmit" class="reset-form">
        <div class="form-group">
          <label for="password">Новый пароль *</label>
          <input
            v-model="form.password"
            id="password"
            type="password"
            placeholder="Минимум 6 символов"
            required
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Подтверждение *</label>
          <input
            v-model="form.confirmPassword"
            id="confirmPassword"
            type="password"
            placeholder="Повторите пароль"
            required
          />
          <small v-if="form.confirmPassword && form.password !== form.confirmPassword" class="error">
            ⚠️ Пароли не совпадают
          </small>
        </div>

        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading || !isValid">
          {{ loading ? 'Сохраняем...' : 'Сохранить пароль' }}
        </button>

        <router-link to="/login" class="back-link">
          ← Вернуться к входу
        </router-link>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref(null)

const isValid = computed(() => {
  return form.value.password && form.value.password === form.value.confirmPassword && form.value.password.length >= 6
})

const handleSubmit = async () => {
  error.value = null
  try {
    loading.value = true
    await authStore.resetPassword(route.params.token, form.value.password)
    alert('✅ Пароль успешно изменен!')
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при сбросе пароля'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 0, 0, 0.1) 100%);
}

.reset-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 1rem;
  padding: 3rem;
  max-width: 400px;
  width: 100%;
}

h1 {
  font-size: 2rem;
  color: #00d4ff;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #b0b0b0;
  text-align: center;
  margin-bottom: 2rem;
}

.reset-form {
  display: flex;
  flex-direction: column;
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
}

input {
  padding: 0.75rem;
  background: #0f0f0f;
  border: 1px solid #333;
  border-radius: 0.5rem;
  color: #e0e0e0;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
}

small {
  margin-top: 0.25rem;
  font-size: 0.85rem;
  color: #ff6b6b;
}

.error-message {
  padding: 1rem;
  background: rgba(255, 107, 107, 0.1);
  border-left: 3px solid #ff6b6b;
  color: #ff6b6b;
  border-radius: 0.25rem;
}

.btn-primary {
  padding: 0.75rem 2rem;
  background: #00d4ff;
  color: #0f0f0f;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #00b8cc;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.back-link {
  text-align: center;
  color: #00d4ff;
  text-decoration: none;
  display: block;
}

.back-link:hover {
  text-decoration: underline;
}
</style>
