import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(false)
  const isAdmin = ref(false)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
    isAuthenticated.value = true
  }

  function clearToken() {
    token.value = null
    localStorage.removeItem('token')
    isAuthenticated.value = false
    isAdmin.value = false
  }

  async function login(credentials) {
    try {
      const response = await api.login(credentials)
      setToken(response.data.token)
      return true
    } catch (error) {
      clearToken()
      throw error
    }
  }

  async function register(user) {
    try {
      await api.register(user)
      return true
    } catch (error) {
      throw error
    }
  }

  return {
    token,
    isAuthenticated,
    isAdmin,
    setToken,
    clearToken,
    login,
    register
  }
})