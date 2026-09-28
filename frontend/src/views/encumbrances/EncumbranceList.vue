<template>
  <div>
    <div class="page-header">
      <h1>Encumbrances</h1>
      <router-link
        v-if="canSubmit"
        to="/encumbrances/new"
        class="btn btn-primary"
      >+ Submit Encumbrance</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Originating Authority</th>
            <th>Title / Parcel</th>
            <th>Status</th>
            <th>Submitted</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in items" :key="e.id">
            <td>{{ e.encumbrance_type }}</td>
            <td>{{ e.originating_authority || '—' }}</td>
            <td>{{ e.title_id || e.parcel_id || '—' }}</td>
            <td><StatusBadge :status="e.status" /></td>
            <td>{{ fmtDate(e.submitted_at) }}</td>
            <td><router-link :to="`/encumbrances/${e.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
          <tr v-if="!items.length">
            <td colspan="6" class="empty">No encumbrances found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { encumbrancesApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const auth  = useAuthStore()
const items = ref([])
const error = ref(null)

const canSubmit = computed(() =>
  auth.isBank || auth.isTaxAuthority || auth.isCourt || auth.isMunicipality ||
  auth.isLawyerNotary || auth.isCitizen || auth.isAdmin
)

onMounted(async () => {
  try { items.value = (await encumbrancesApi.list()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load encumbrances' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
