<template>
  <div>
    <div class="page-header">
      <h1>Title Applications</h1>
      <router-link
        v-if="auth.isLawyerNotary || auth.isCitizen || auth.isAdmin"
        to="/titles/applications/new"
        class="btn btn-primary"
      >+ New Application</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Parcel ID</th>
            <th>Instrument Type</th>
            <th>Proposed Owner</th>
            <th>Status</th>
            <th>Submitted</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in apps" :key="a.id">
            <td>{{ a.parcel_id.substring(0,8) }}…</td>
            <td>{{ a.instrument_type }}</td>
            <td>{{ a.proposed_owner_name }}</td>
            <td><StatusBadge :status="a.status" /></td>
            <td>{{ fmtDate(a.submitted_at) }}</td>
            <td><router-link :to="`/titles/applications/${a.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
          <tr v-if="!apps.length">
            <td colspan="6" class="empty">No applications found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { titlesApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const auth  = useAuthStore()
const apps  = ref([])
const error = ref(null)

onMounted(async () => {
  try { apps.value = (await titlesApi.listApplications()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load applications' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
