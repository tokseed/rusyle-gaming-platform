import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const api = axios.create({
  baseURL: '/api'
})

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  if (token.value) {
    api.defaults.headers.common.Authorization = `Bearer ${token.value}`
  }

  const setAuthData = (userData, authToken) => {
    user.value = userData
    token.value = authToken
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('token', authToken)
    api.defaults.headers.common.Authorization = `Bearer ${authToken}`
  }

  const clearAuthData = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    delete api.defaults.headers.common.Authorization
  }

  const login = async (email, password) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/auth/login', { email, password })
      setAuthData(data.user, data.access_token)
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка входа'
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (fullName, email, password) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/auth/register', {
        full_name: fullName,
        email,
        password
      })
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка регистрации'
      throw err
    } finally {
      loading.value = false
    }
  }

  const verifyEmail = async (tokenStr) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/auth/verify-email', { token: tokenStr })
      if (data.user && data.access_token) {
        setAuthData(data.user, data.access_token)
      }
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка верификации'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch {
      // игнорим
    } finally {
      clearAuthData()
    }
  }

  const forgotPassword = async (email) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/auth/forgot-password', { email })
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка восстановления пароля'
      throw err
    } finally {
      loading.value = false
    }
  }

  const resetPassword = async (tokenStr, password) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/auth/reset-password', {
        token: tokenStr,
        password
      })
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка сброса пароля'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    register,
    verifyEmail,
    logout,
    forgotPassword,
    resetPassword,
    setAuthData,
    clearAuthData
  }
})
