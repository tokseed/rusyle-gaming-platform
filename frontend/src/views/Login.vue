<template>
  <div class="login-container">
    <div class="login-card">
      <h1>🎮 RuSyle</h1>
      <h2>Вход в систему</h2>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            v-model="email"
            id="email"
            type="email"
            placeholder="your@email.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            v-model="password"
            id="password"
            type="password"
            placeholder="••••••••"
            required
          />
        </div>

        <button type="submit" class="btn-primary" :disabled="authStore.loading">
          {{ authStore.loading ? 'Вход...' : 'Вход' }}
        </button>

        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>
      </form>

      <div class="links">
        <router-link to="/forgot-password">Забыли пароль?</router-link>
        <span>или</span>
        <router-link to="/register">Создать аккаунт</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    await authStore.login(email.value, password.value)
    router.push('/events')
  } catch (err) {
    console.error('Ошибка входа:', err)
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
}

.login-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 1rem;
  padding: 3rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.1);
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #00d4ff;
}

h2 {
  text-align: center;
  color: #e0e0e0;
  margin-bottom: 2rem;
  font-size: 1.3rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #b0b0b0;
}

input {
  width: 100%;
  padding: 0.75rem;
  background: #0f0f0f;
  border: 1px solid #333;
  border-radius: 0.5rem;
  color: #e0e0e0;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #00d4ff;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #00d4ff;
  color: #0f0f0f;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #00b8cc;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(255, 107, 107, 0.1);
  border-left: 3px solid #ff6b6b;
  color: #ff6b6b;
  border-radius: 0.25rem;
}

.links {
  margin-top: 2rem;
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #b0b0b0;
}

.links a {
  color: #00d4ff;
  text-decoration: none;
  transition: color 0.3s;
}

.links a:hover {
  color: #00b8cc;
}

@media (max-width: 600px) {
  .login-card {
    padding: 2rem;
  }

  h1 {
    font-size: 1.5rem;
  }
}
</style>
