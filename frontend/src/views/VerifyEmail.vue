<template>
  <div class="verify-container">
    <div class="verify-card">
      <div v-if="loading" class="state-loading">
        <div class="spinner"></div>
        <h1>⏳ Проверяем email...</h1>
        <p>Подождите, идет подтверждение</p>
      </div>

      <div v-if="!loading && success" class="state-success">
        <h1>✅ Email подтвержден!</h1>
        <p>Ваш аккаунт успешно активирован</p>
        <router-link to="/login" class="btn-primary">
          Перейти к входу
        </router-link>
      </div>

      <div v-if="!loading && error" class="state-error">
        <h1>❌ Ошибка подтверждения</h1>
        <p>{{ error }}</p>
        <router-link to="/register" class="btn-primary">
          Вернуться на регистрацию
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'

const route = useRoute()
const authStore = useAuthStore()

const loading = ref(true)
const success = ref(false)
const error = ref(null)

onMounted(async () => {
  try {
    await authStore.verifyEmail(route.params.token)
    success.value = true
  } catch (err) {
    error.value = err.response?.data?.error || 'Неверная или истекшая ссылка'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.verify-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 0, 0, 0.1) 100%);
}

.verify-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 1rem;
  padding: 3rem;
  max-width: 400px;
  width: 100%;
  text-align: center;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

p {
  color: #b0b0b0;
  margin-bottom: 2rem;
}

.state-loading h1 {
  color: #00d4ff;
}

.state-success h1 {
  color: #4caf50;
}

.state-error h1 {
  color: #ff6b6b;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #333;
  border-top-color: #00d4ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn-primary {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: #00d4ff;
  color: #0f0f0f;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}
</style>
