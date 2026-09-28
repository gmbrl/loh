import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue'), meta: { public: true } },

  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },

  // Parcels & Surveys
  { path: '/parcels', name: 'Parcels', component: () => import('../views/parcels/ParcelList.vue') },
  { path: '/parcels/surveys', name: 'Surveys', component: () => import('../views/parcels/SurveyList.vue') },
  { path: '/parcels/surveys/new', name: 'SurveyNew', component: () => import('../views/parcels/SurveyForm.vue') },
  { path: '/parcels/surveys/:id', name: 'SurveyDetail', component: () => import('../views/parcels/SurveyDetail.vue') },
  { path: '/parcels/new', name: 'ParcelNew', component: () => import('../views/parcels/ParcelForm.vue') },
  { path: '/parcels/:id', name: 'ParcelDetail', component: () => import('../views/parcels/ParcelDetail.vue') },

  // Titles
  { path: '/titles', name: 'Titles', component: () => import('../views/titles/TitleList.vue') },
  { path: '/titles/applications', name: 'TitleApplications', component: () => import('../views/titles/TitleApplicationList.vue') },
  { path: '/titles/applications/new', name: 'TitleApplicationNew', component: () => import('../views/titles/TitleApplicationForm.vue') },
  { path: '/titles/applications/:id', name: 'TitleApplicationDetail', component: () => import('../views/titles/TitleApplicationDetail.vue') },
  { path: '/titles/:id', name: 'TitleDetail', component: () => import('../views/titles/TitleDetail.vue') },

  // Encumbrances
  { path: '/encumbrances', name: 'Encumbrances', component: () => import('../views/encumbrances/EncumbranceList.vue') },
  { path: '/encumbrances/new', name: 'EncumbranceNew', component: () => import('../views/encumbrances/EncumbranceForm.vue') },
  { path: '/encumbrances/:id', name: 'EncumbranceDetail', component: () => import('../views/encumbrances/EncumbranceDetail.vue') },

  // Corrections
  { path: '/corrections', name: 'Corrections', component: () => import('../views/corrections/CorrectionList.vue') },
  { path: '/corrections/new', name: 'CorrectionNew', component: () => import('../views/corrections/CorrectionForm.vue') },
  { path: '/corrections/:id', name: 'CorrectionDetail', component: () => import('../views/corrections/CorrectionDetail.vue') },

  // Query
  { path: '/query', name: 'Query', component: () => import('../views/query/QueryView.vue') },

  // Admin
  { path: '/admin/users', name: 'Users', component: () => import('../views/admin/UserList.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }
})

export default router
