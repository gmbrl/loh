<template>
  <div>
    <div class="page-header">
      <h1>Title Detail</h1>
      <router-link to="/titles" class="btn btn-ghost">← Back</router-link>
    </div>
    <div v-if="error" class="alert alert-error">{{ error }}</div>

    <div v-if="title" class="card">
      <h2>{{ title.title_number }}</h2>
      <table class="data-table mt-2">
        <tbody>
          <tr><td><strong>Owner</strong></td><td>{{ title.owner_name }}</td></tr>
          <tr><td><strong>Parcel</strong></td><td>
            <router-link :to="`/parcels/${title.parcel_id}`">{{ title.parcel_id }}</router-link>
          </td></tr>
          <tr><td><strong>Status</strong></td><td><StatusBadge :status="title.status" /></td></tr>
          <tr><td><strong>Registered At</strong></td><td>{{ fmtDate(title.registered_at) }}</td></tr>
          <tr><td><strong>Application</strong></td><td>
            <router-link :to="`/titles/applications/${title.application_id}`">{{ title.application_id }}</router-link>
          </td></tr>
        </tbody>
      </table>
    </div>

    <!-- History -->
    <div v-if="history.length" class="card">
      <h3>History</h3>
      <table class="data-table">
        <thead><tr><th>Event</th><th>Detail</th><th>Date</th></tr></thead>
        <tbody>
          <tr v-for="h in history" :key="h.id">
            <td>{{ h.event }}</td>
            <td>{{ h.detail || '—' }}</td>
            <td>{{ fmtDate(h.recorded_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Encumbrances on this title -->
    <div v-if="encumbrances.length" class="card">
      <h3>Registered Encumbrances</h3>
      <table class="data-table">
        <thead><tr><th>Type</th><th>Authority</th><th>Status</th><th>Date</th><th></th></tr></thead>
        <tbody>
          <tr v-for="e in encumbrances" :key="e.id">
            <td>{{ e.encumbrance_type }}</td>
            <td>{{ e.originating_authority || '—' }}</td>
            <td><StatusBadge :status="e.status" /></td>
            <td>{{ fmtDate(e.submitted_at) }}</td>
            <td><router-link :to="`/encumbrances/${e.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { titlesApi, queryApi } from '../../api/index.js'
import StatusBadge from '../../components/StatusBadge.vue'

const route        = useRoute()
const title        = ref(null)
const history      = ref([])
const encumbrances = ref([])
const error        = ref(null)

onMounted(async () => {
  try {
    const id = route.params.id
    title.value        = (await titlesApi.get(id)).data
    history.value      = (await titlesApi.history(id)).data
    encumbrances.value = (await queryApi.encumbrances({ title_id: id })).data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load title'
  }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
