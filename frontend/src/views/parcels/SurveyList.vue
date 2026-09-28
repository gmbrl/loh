<template>
  <div>
    <div class="page-header">
      <h1>Survey Plans</h1>
      <router-link v-if="auth.isSurveyor || auth.isAdmin" to="/parcels/surveys/new" class="btn btn-primary">
        + Submit Survey Plan
      </router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Reference</th>
            <th>Area (m²)</th>
            <th>Status</th>
            <th>Submitted</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in surveys" :key="s.id">
            <td>{{ s.reference_number }}</td>
            <td>{{ s.area_sqm?.toLocaleString() || '—' }}</td>
            <td><StatusBadge :status="s.status" /></td>
            <td>{{ fmtDate(s.submitted_at) }}</td>
            <td>
              <router-link :to="`/parcels/surveys/${s.id}`" class="btn btn-ghost">View</router-link>
            </td>
          </tr>
          <tr v-if="!surveys.length">
            <td colspan="5" class="empty">No survey plans found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { parcelsApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const auth    = useAuthStore()
const surveys = ref([])
const error   = ref(null)

onMounted(async () => {
  try { surveys.value = (await parcelsApi.listSurveys()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load surveys' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
