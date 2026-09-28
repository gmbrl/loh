import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      const auth = useAuthStore()
      auth.logout()
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authApi = {
  login: (email, password) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return api.post('/auth/login', form)
  },
  me: () => api.get('/auth/me'),
}

// ── Users ─────────────────────────────────────────────────────────────────────
export const usersApi = {
  list: () => api.get('/users/'),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.patch(`/users/${id}`, data),
}

// ── Parcels ───────────────────────────────────────────────────────────────────
export const parcelsApi = {
  list: () => api.get('/parcels/'),
  get: (id) => api.get(`/parcels/${id}`),
  create: (data) => api.post('/parcels/', data),

  listSurveys: () => api.get('/parcels/surveys'),
  getSurvey: (id) => api.get(`/parcels/surveys/${id}`),
  submitSurvey: (data) => api.post('/parcels/surveys', data),
  reviewSurvey: (id, data) => api.post(`/parcels/surveys/${id}/review`, data),
}

// ── Titles ────────────────────────────────────────────────────────────────────
export const titlesApi = {
  list: () => api.get('/titles/'),
  get: (id) => api.get(`/titles/${id}`),
  history: (id) => api.get(`/titles/${id}/history`),

  listApplications: () => api.get('/titles/applications'),
  getApplication: (id) => api.get(`/titles/applications/${id}`),
  createApplication: (data) => api.post('/titles/applications', data),
  decideApplication: (id, data) => api.post(`/titles/applications/${id}/decide`, data),
}

// ── Encumbrances ──────────────────────────────────────────────────────────────
export const encumbrancesApi = {
  list: () => api.get('/encumbrances/'),
  get: (id) => api.get(`/encumbrances/${id}`),
  submit: (data) => api.post('/encumbrances/', data),
  approve: (id) => api.post(`/encumbrances/${id}/approve`),
  release: (id, data) => api.post(`/encumbrances/${id}/release`, data),
}

// ── Corrections ───────────────────────────────────────────────────────────────
export const correctionsApi = {
  list: () => api.get('/corrections/'),
  get: (id) => api.get(`/corrections/${id}`),
  submit: (data) => api.post('/corrections/', data),
  review: (id, data) => api.post(`/corrections/${id}/review`, data),
}

// ── Query ─────────────────────────────────────────────────────────────────────
export const queryApi = {
  parcels: (params) => api.get('/query/parcels', { params }),
  titles: (params) => api.get('/query/titles', { params }),
  encumbrances: (params) => api.get('/query/encumbrances', { params }),
}
