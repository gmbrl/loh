<template>
  <div>
    <div class="page-header">
      <h1>Correction Requests</h1>
      <router-link
        v-if="canSubmit"
        to="/corrections/new"
        class="btn btn-primary"
      >+ New Correction</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Level</th>
            <th>Description</th>
            <th>Parcel / Title</th>
            <th>Status</th>
            <th>Submitted</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in items" :key="c.id">
            <td>{{ c.correction_level }}</td>
            <td>{{ c.description.substring(0,60) }}{{ c.description.length > 60 ? '…' : '' }}</td>
            <td>{{ c.parcel_id || c.title_id || '—' }}</td>
            <td><StatusBadge :status="c.status" /></td>
            <td>{{ fmtDate(c.submitted_at) }}</td>
            <td><router-link :to="`/corrections/${c.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="6" class="empty">No correction requests found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { correctionsApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const auth  = useAuthStore()
const items = ref([])
const error = ref(null)

const canSubmit = computed(() =>
  auth.isSurveyor || auth.isCadastral || auth.isRegistrar || auth.isCourt || auth.isAdmin
)

onMounted(async () => {
  try { items.value = (await correctionsApi.list()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load corrections' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
