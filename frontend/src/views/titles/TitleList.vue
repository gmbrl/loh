<template>
  <div>
    <div class="page-header">
      <h1>Titles</h1>
    </div>
    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Title No.</th>
            <th>Owner</th>
            <th>Parcel ID</th>
            <th>Status</th>
            <th>Registered</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in titles" :key="t.id">
            <td>{{ t.title_number }}</td>
            <td>{{ t.owner_name }}</td>
            <td><router-link :to="`/parcels/${t.parcel_id}`">{{ t.parcel_id.substring(0,8) }}…</router-link></td>
            <td><StatusBadge :status="t.status" /></td>
            <td>{{ fmtDate(t.registered_at) }}</td>
            <td><router-link :to="`/titles/${t.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
          <tr v-if="!titles.length">
            <td colspan="6" class="empty">No titles registered.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { titlesApi } from '../../api/index.js'
import StatusBadge from '../../components/StatusBadge.vue'

const titles = ref([])
const error  = ref(null)

onMounted(async () => {
  try { titles.value = (await titlesApi.list()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load titles' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
