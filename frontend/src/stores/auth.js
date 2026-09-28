import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/index.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user  = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const role = computed(() => user.value?.role || null)

  // Role helpers
  const can = (roles) => roles.includes(role.value)
  const isAdmin           = computed(() => role.value === 'admin')
  const isSurveyor        = computed(() => role.value === 'surveyor')
  const isCadastral       = computed(() => role.value === 'cadastral_officer')
  const isRegistrar       = computed(() => role.value === 'registrar')
  const isLawyerNotary    = computed(() => role.value === 'lawyer_notary')
  const isBank            = computed(() => role.value === 'bank')
  const isTaxAuthority    = computed(() => role.value === 'tax_authority')
  const isCourt           = computed(() => role.value === 'court')
  const isMunicipality    = computed(() => role.value === 'municipality')
  const isCitizen         = computed(() => role.value === 'citizen')

  async function login(email, password) {
    const { data } = await authApi.login(email, password)
    token.value = data.access_token
    user.value  = data.user
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token, user, isAuthenticated, role,
    can,
    isAdmin, isSurveyor, isCadastral, isRegistrar,
    isLawyerNotary, isBank, isTaxAuthority, isCourt,
    isMunicipality, isCitizen,
    login, logout,
  }
})
