<template>
  <div class="register-container">
    <div class="register-card">
      <div class="card-header">
        <h1>📝 Регистрация</h1>
        <p class="subtitle">Создайте аккаунт в RuSyle</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- ФИО -->
        <div class="form-group">
          <label for="fullName">Полное имя *</label>
          <input
            v-model="form.fullName"
            id="fullName"
            type="text"
            placeholder="Иван Петров"
            required
          />
        </div>

        <!-- Email -->
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

        <!-- Пароль -->
        <div class="form-group">
          <label for="password">Пароль *</label>
          <input
            v-model="form.password"
            id="password"
            type="password"
            placeholder="Минимум 6 символов"
            required
          />
          <small v-if="form.password.length > 0" class="password-strength">
            Длина: {{ form.password.length }} символов
            <span
              :class="{
                'strength-weak': form.password.length < 8,
                'strength-medium': form.password.length >= 8 && form.password.length < 12,
                'strength-strong': form.password.length >= 12
              }"
            >
              {{
                form.password.length < 8
                  ? '(слабый)'
                  : form.password.length < 12
                  ? '(средний)'
                  : '(сильный)'
              }}
            </span>
          </small>
        </div>

        <!-- Подтверждение пароля -->
        <div class="form-group">
          <label for="confirmPassword">Подтверждение пароля *</label>
          <input
            v-model="form.confirmPassword"
            id="confirmPassword"
            type="password"
            placeholder="Повторите пароль"
            required
          />
          <small
            v-if="form.confirmPassword && form.password !== form.confirmPassword"
            class="password-error"
          >
            ⚠️ Пароли не совпадают
          </small>
        </div>

        <!-- Согласие с условиями -->
        <div class="form-group checkbox">
          <input
            v-model="form.agreeTerms"
            id="agreeTerms"
            type="checkbox"
            required
          />
          <label for="agreeTerms" class="checkbox-label">
            Я согласен с
            <a href="#" class="link">условиями использования</a>
            и
            <a href="#" class="link">политикой конфиденциальности</a>
          </label>
        </div>

        <!-- Ошибки -->
        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <!-- Кнопка -->
        <button type="submit" class="btn-primary" :disabled="loading || !isFormValid">
          {{ loading ? 'Создание аккаунта...' : 'Зарегистрироваться' }}
        </button>

        <!-- Ссылка на вход -->
        <div class="auth-link">
          Уже есть аккаунт?
          <router-link to="/login" class="link">Войти</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const loading = ref(false)
const error = ref(null)

const isFormValid = computed(() => {
  return (
    form.value.fullName &&
    form.value.email &&
    form.value.password &&
    form.value.password === form.value.confirmPassword &&
    form.value.password.length >= 6 &&
    form.value.agreeTerms
  )
})

const handleRegister = async () => {
  error.value = null

  try {
    loading.value = true
    await authStore.register(
      form.value.fullName,
      form.value.email,
      form.value.password
    )

    // Успешно! Показываем сообщение
    alert('✅ Регистрация успешна! Проверьте свой email для подтверждения.')
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при регистрации'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 0, 0, 0.1) 100%);
}

.register-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 1rem;
  padding: 3rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.card-header h1 {
  font-size: 2rem;
  color: #00d4ff;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #b0b0b0;
  font-size: 0.95rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: flex-start;
  gap: 0.75rem;
}

label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #b0b0b0;
  font-size: 0.95rem;
}

.checkbox-label {
  margin-bottom: 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

input[type='text'],
input[type='email'],
input[type='password'] {
  padding: 0.75rem;
  background: #0f0f0f;
  border: 1px solid #333;
  border-radius: 0.5rem;
  color: #e0e0e0;
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input[type='text']:focus,
input[type='email']:focus,
input[type='password']:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
}

input[type='checkbox'] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  margin-top: 2px;
}

small {
  margin-top: 0.25rem;
  font-size: 0.8rem;
  color: #707070;
}

.password-strength {
  color: #b0b0b0;
}

.strength-weak {
  color: #ff6b6b;
}

.strength-medium {
  color: #ffc107;
}

.strength-strong {
  color: #4caf50;
}

.password-error {
  color: #ff6b6b;
}

.link {
  color: #00d4ff;
  text-decoration: none;
  transition: color 0.3s;
}

.link:hover {
  color: #00b8cc;
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
  font-size: 1rem;
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

.auth-link {
  text-align: center;
  color: #b0b0b0;
  font-size: 0.95rem;
}

.auth-link .link {
  margin-left: 0.25rem;
}

@media (max-width: 600px) {
  .register-card {
    padding: 2rem 1.5rem;
  }

  .card-header h1 {
    font-size: 1.5rem;
  }
}
</style>
