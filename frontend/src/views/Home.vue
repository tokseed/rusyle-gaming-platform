<template>
  <div class="home-container">
    <section class="hero">
      <h1> RuSyle</h1>
      <p class="tagline">Платформа российской игровой индустрии</p>
      <p class="description">
        Единое пространство для популяризации отечественных игровых проектов
      </p>

      <div class="cta-buttons">
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="btn-primary">
          Вход в систему
        </router-link>
        <router-link v-if="!authStore.isAuthenticated" to="/register" class="btn-secondary">
          Создать аккаунт
        </router-link>
        <router-link v-if="authStore.isAuthenticated" to="/events" class="btn-primary">
          Смотреть события
        </router-link>
      </div>
    </section>

    <section class="features">
      <h2>Основные функции</h2>
      <div class="features-grid">
        <div class="feature">
          <span class="icon">🔐</span>
          <h3>Безопасная авторизация</h3>
          <p>Регистрация с подтверждением email, восстановление пароля</p>
        </div>

        <div class="feature">
          <span class="icon">📅</span>
          <h3>Управление событиями</h3>
          <p>Просмотр активных, прошедших и ваших событий</p>
        </div>

        <div class="feature">
          <span class="icon">⚙️</span>
          <h3>Администрирование</h3>
          <p>Управление пользователями и экспорт данных (для админов)</p>
        </div>

        <div class="feature">
          <span class="icon">💬</span>
          <h3>Отзывы и рейтинги</h3>
          <p>Оставляйте отзывы на события и смотрите оценки других</p>
        </div>
      </div>
    </section>

    <section v-if="authStore.isAuthenticated" class="welcome">
      <h2>Добро пожаловать, {{ authStore.user?.full_name }}! 👋</h2>
      <p>Изучите мир российских игровых проектов и будьте в курсе всех событий индустрии</p>
    </section>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth.js'

const authStore = useAuthStore()
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 212, 255, 0.05) 100%);
  border-radius: 1rem;
  margin-bottom: 3rem;
}

h1 {
  font-size: 3rem;
  color: #00d4ff;
  margin-bottom: 1rem;
}

.tagline {
  font-size: 1.5rem;
  color: #e0e0e0;
  margin-bottom: 0.5rem;
}

.description {
  font-size: 1.1rem;
  color: #b0b0b0;
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  display: inline-block;
}

.btn-primary {
  background: #00d4ff;
  color: #0f0f0f;
}

.btn-primary:hover {
  background: #00b8cc;
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: #00d4ff;
  border: 2px solid #00d4ff;
}

.btn-secondary:hover {
  background: rgba(0, 212, 255, 0.1);
}

.features {
  margin-bottom: 3rem;
}

.features h2 {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 2rem;
  color: #e0e0e0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature {
  background: #1a1a1a;
  border: 1px solid #333;
  padding: 2rem;
  border-radius: 0.75rem;
  text-align: center;
  transition: all 0.3s;
}

.feature:hover {
  border-color: #00d4ff;
  box-shadow: 0 8px 25px rgba(0, 212, 255, 0.1);
}

.icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.feature h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #e0e0e0;
}

.feature p {
  color: #b0b0b0;
  font-size: 0.95rem;
}

.welcome {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
  padding: 2rem;
  border-radius: 0.75rem;
  text-align: center;
  border: 1px solid #4caf50;
}

.welcome h2 {
  color: #4caf50;
  margin-bottom: 0.5rem;
}

.welcome p {
  color: #b0b0b0;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1.2rem;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
