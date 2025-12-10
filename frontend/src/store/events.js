import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from './auth.js'

export const useEventsStore = defineStore('events', () => {
  const events = ref([])
  const currentEvent = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const activeEvents = computed(() =>
    events.value.filter(e => e.status === 'active')
  )

  const pastEvents = computed(() =>
    events.value.filter(e => e.status === 'past')
  )

  const myEvents = computed(() =>
    events.value.filter(e => e.is_participant === true)
  )

  const fetchEvents = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get('/events', { params })
      events.value = data
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка загрузки событий'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchEventById = async (id) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get(`/events/${id}`)
      currentEvent.value = data
      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Ошибка загрузки события'
      throw err
    } finally {
      loading.value = false
    }
  }

  const participate = async (eventId) => {
    try {
      const { data } = await api.post(`/events/${eventId}/participate`)
      const index = events.value.findIndex(e => e.id === eventId)
      if (index !== -1) events.value[index] = data
      if (currentEvent.value?.id === eventId) currentEvent.value = data
      return data
    } catch (err) {
      throw err
    }
  }

  const cancelParticipation = async (eventId) => {
    try {
      const { data } = await api.post(`/events/${eventId}/cancel-participation`)
      const index = events.value.findIndex(e => e.id === eventId)
      if (index !== -1) events.value[index] = data
      if (currentEvent.value?.id === eventId) currentEvent.value = data
      return data
    } catch (err) {
      throw err
    }
  }

  const addReview = async (eventId, rating, text) => {
    try {
      const { data } = await api.post(`/events/${eventId}/review`, {
        rating,
        text
      })
      return data
    } catch (err) {
      throw err
    }
  }

  return {
    events,
    currentEvent,
    loading,
    error,
    activeEvents,
    pastEvents,
    myEvents,
    fetchEvents,
    fetchEventById,
    participate,
    cancelParticipation,
    addReview
  }
})
