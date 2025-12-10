<template>
  <div class="forgot-container">
    <div class="forgot-card">
      <h1>🔑 Восстановление пароля</h1>
      <p class="subtitle">Введите email, чтобы получить ссылку для сброса</p>

      <form @submit.prevent="handleSubmit" class="forgot-form">
        <div class="form-group">
          <label for="email">Email *</label>
          <input
            v-model="form.email"
            id="email"
            type="email"
            placeholder="your@email.com"
            required
          />
        </div>

        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <div v-if="success" class="success-message">
          ✅ Письмо отправлено! Проверьте почту
        </div>

        <button type="submit" class="btn-primary" :disabled="loading || success">
          {{ loading ? 'Отправляем...' : 'Отправить' }}
        </button>

        <router-link to="/login" class="back-link">
          ← Вернуться к входу
        </router-link>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth.js'

const authStore = useAuthStore()

const form = ref({ email: '' })
const loading = ref(false)
const error = ref(null)
const success = ref(false)

const handleSubmit = async () => {
  error.value = null
  try {
    loading.value = true
    await authStore.forgotPassword(form.value.email)
    success.value = true
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при отправке'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.forgot-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 0, 0, 0.1) 100%);
}

.forgot-card {
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

.forgot-form {
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

.error-message {
  padding: 1rem;
  background: rgba(255, 107, 107, 0.1);
  border-left: 3px solid #ff6b6b;
  color: #ff6b6b;
  border-radius: 0.25rem;
}

.success-message {
  padding: 1rem;
  background: rgba(76, 175, 80, 0.1);
  border-left: 3px solid #4caf50;
  color: #4caf50;
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
  margin-top: 1rem;
}

.back-link:hover {
  text-decoration: underline;
}
</style>
