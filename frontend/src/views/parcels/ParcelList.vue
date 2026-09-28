<template>
  <div>
    <div class="page-header">
      <h1>Parcels</h1>
      <router-link v-if="auth.isCadastral || auth.isAdmin" to="/parcels/new" class="btn btn-primary">
        + Create Parcel
      </router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Identifier</th>
            <th>Description</th>
            <th>Area (m²)</th>
            <th>Land Use</th>
            <th>Status</th>
            <th>Created</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in parcels" :key="p.id">
            <td>{{ p.parcel_identifier }}</td>
            <td>{{ p.description || '—' }}</td>
            <td>{{ p.area_sqm?.toLocaleString() || '—' }}</td>
            <td>{{ p.land_use || '—' }}</td>
            <td><StatusBadge :status="p.status" /></td>
            <td>{{ fmtDate(p.created_at) }}</td>
            <td>
              <router-link :to="`/parcels/${p.id}`" class="btn btn-ghost">View</router-link>
            </td>
          </tr>
          <tr v-if="!parcels.length">
            <td colspan="7" class="empty">No parcels found.</td>
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
const parcels = ref([])
const error   = ref(null)

onMounted(async () => {
  try { parcels.value = (await parcelsApi.list()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load parcels' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
