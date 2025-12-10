<template>
  <div class="auth-container">
    <!-- РЕГИСТРАЦИЯ -->
    <div v-if="!isLogin" class="auth-form">
      <div class="auth-header">
        <h1>📝 Регистрация</h1>
        <p>Создайте аккаунт в RuSyle</p>
      </div>

      <form @submit.prevent="register" class="form">
        <div class="form-group">
          <label for="full_name">Полное имя *</label>
          <input
            v-model="form.full_name"
            type="text"
            id="full_name"
            placeholder="Ваше имя"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Email *</label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            placeholder="example@gmail.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Пароль *</label>
          <input
            v-model="form.password"
            type="password"
            id="password"
            placeholder="Минимум 6 символов"
            required
          />
          <small>Длина: {{ form.password.length }} символов (средний)</small>
        </div>

        <div class="form-group">
          <label for="confirm_password">Подтвердить пароль *</label>
          <input
            v-model="form.confirm_password"
            type="password"
            id="confirm_password"
            placeholder="Повторите пароль"
            required
          />
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <!-- Успех -->
        <div v-if="success" class="success-message">
          ✅ {{ success }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>

        <p class="toggle-link">
          Уже есть аккаунт?
          <a href="#" @click.prevent="toggleForm">Войти</a>
        </p>
      </form>
    </div>

    <!-- ВХОД -->
    <div v-else class="auth-form">
      <div class="auth-header">
        <h1>🔑 Вход</h1>
        <p>Добро пожаловать в RuSyle</p>
      </div>

      <form @submit.prevent="login" class="form">
        <div class="form-group">
          <label for="login_email">Email *</label>
          <input
            v-model="form.email"
            type="email"
            id="login_email"
            placeholder="example@gmail.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="login_password">Пароль *</label>
          <input
            v-model="form.password"
            type="password"
            id="login_password"
            placeholder="Ваш пароль"
            required
          />
        </div>

        <!-- Ошибка -->
        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <!-- Успех -->
        <div v-if="success" class="success-message">
          ✅ {{ success }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Войти' }}
        </button>

        <p class="toggle-link">
          Нет аккаунта?
          <a href="#" @click.prevent="toggleForm">Зарегистрироваться</a>
        </p>
      </form>

      <!-- Если залогинены -->
      <div v-if="currentUser" class="user-profile">
        <h2>✅ Вы залогинены!</h2>
        <div class="user-info">
          <p><strong>Имя:</strong> {{ currentUser.full_name }}</p>
          <p><strong>Email:</strong> {{ currentUser.email }}</p>
          <p><strong>ID:</strong> {{ currentUser.id }}</p>
        </div>
        <button @click="logout" class="btn-secondary">Выйти</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')
const success = ref('')
const currentUser = ref(null)

const form = ref({
  full_name: '',
  email: '',
  password: '',
  confirm_password: ''
})

const API_URL = 'http://127.0.0.1:5000/api'

// Переключение между формами
const toggleForm = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  success.value = ''
  form.value = { full_name: '', email: '', password: '', confirm_password: '' }
}

// РЕГИСТРАЦИЯ
const register = async () => {
  error.value = ''
  success.value = ''

  // Проверяем пароли
  if (form.value.password !== form.value.confirm_password) {
    error.value = 'Пароли не совпадают'
    return
  }

  if (form.value.password.length < 6) {
    error.value = 'Пароль должен быть минимум 6 символов'
    return
  }

  loading.value = true

  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        full_name: form.value.full_name,
        email: form.value.email,
        password: form.value.password
      })
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Ошибка регистрации'
      return
    }

    success.value = '✅ Регистрация успешна! Переходим к входу...'
    
    setTimeout(() => {
      isLogin.value = true
      form.value = { full_name: '', email: '', password: '', confirm_password: '' }
      success.value = ''
    }, 2000)
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// ВХОД
const login = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: form.value.email,
        password: form.value.password
      })
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Ошибка входа'
      return
    }

    // Сохраняем токен
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user))

    success.value = '✅ Успешный вход!'
    currentUser.value = data.user

    setTimeout(() => {
      form.value = { full_name: '', email: '', password: '', confirm_password: '' }
      success.value = ''
    }, 2000)
  } catch (err) {
    error.value = 'Ошибка подключения к серверу'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// ВЫХОД
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  currentUser.value = null
  isLogin.value = true
}

// Проверяем, залогинены ли мы
onMounted(() => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    currentUser.value = JSON.parse(user)
  }
})
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-form {
  background: #0f3460;
  border-radius: 12px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid #00d4ff;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h1 {
  color: #00d4ff;
  font-size: 28px;
  margin: 0 0 10px 0;
}

.auth-header p {
  color: #a0a0a0;
  margin: 0;
  font-size: 14px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #e0e0e0;
  font-weight: 600;
  font-size: 14px;
}

.form-group input {
  padding: 12px 15px;
  border: 1px solid #333;
  border-radius: 6px;
  background: #1a1a2e;
  color: #e0e0e0;
  font-size: 14px;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

.form-group small {
  color: #707070;
  font-size: 12px;
}

.error-message {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid #ff6b6b;
  color: #ff6b6b;
  padding: 12px 15px;
  border-radius: 6px;
  font-size: 14px;
}

.success-message {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid #4caf50;
  color: #4caf50;
  padding: 12px 15px;
  border-radius: 6px;
  font-size: 14px;
}

.btn-primary {
  padding: 12px 20px;
  background: #00d4ff;
  color: #0f3460;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #00b8cc;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 10px 20px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: #ff5252;
}

.toggle-link {
  text-align: center;
  color: #a0a0a0;
  font-size: 14px;
  margin: 0;
}

.toggle-link a {
  color: #00d4ff;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.toggle-link a:hover {
  color: #00b8cc;
}

.user-profile {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid #4caf50;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.user-profile h2 {
  color: #4caf50;
  margin-top: 0;
}

.user-info {
  background: rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 15px;
  color: #e0e0e0;
}

.user-info p {
  margin: 8px 0;
  font-size: 14px;
}

@media (max-width: 600px) {
  .auth-form {
    padding: 25px;
  }

  .auth-header h1 {
    font-size: 24px;
  }
}
</style>
