<template>
  <div>
    <div class="page-header">
      <h1>Parcel Detail</h1>
      <router-link to="/parcels" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="parcel" class="card">
      <h2>{{ parcel.parcel_identifier }}</h2>
      <table class="data-table mt-2">
        <tbody>
          <tr><td><strong>ID</strong></td><td>{{ parcel.id }}</td></tr>
          <tr><td><strong>Description</strong></td><td>{{ parcel.description || '—' }}</td></tr>
          <tr><td><strong>Area (m²)</strong></td><td>{{ parcel.area_sqm?.toLocaleString() || '—' }}</td></tr>
          <tr><td><strong>Land Use</strong></td><td>{{ parcel.land_use || '—' }}</td></tr>
          <tr><td><strong>Status</strong></td><td><StatusBadge :status="parcel.status" /></td></tr>
          <tr><td><strong>Survey Plan</strong></td><td>
            <router-link :to="`/parcels/surveys/${parcel.survey_plan_id}`">{{ parcel.survey_plan_id }}</router-link>
          </td></tr>
          <tr><td><strong>Created</strong></td><td>{{ fmtDate(parcel.created_at) }}</td></tr>
          <tr><td><strong>Geometry (WKT/GeoJSON)</strong></td><td><code style="font-size:11px">{{ parcel.geometry || '—' }}</code></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { parcelsApi } from '../../api/index.js'
import StatusBadge from '../../components/StatusBadge.vue'

const route  = useRoute()
const parcel = ref(null)
const error  = ref(null)

onMounted(async () => {
  try { parcel.value = (await parcelsApi.get(route.params.id)).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load parcel' }
})

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
