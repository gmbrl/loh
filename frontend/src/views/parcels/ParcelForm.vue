<template>
  <div>
    <div class="page-header">
      <h1>Create Official Parcel</h1>
      <router-link to="/parcels" class="btn btn-ghost">← Back</router-link>
    </div>
    <div class="alert alert-info">
      Only approved survey plans can be used. The official parcel is activated here by a cadastral officer.
    </div>

    <div v-if="error" class="alert alert-error mt-2">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-2">Parcel created successfully.</div>

    <div class="card mt-2">
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Parcel Identifier *</label>
          <input v-model="form.parcel_identifier" required />
        </div>
        <div class="form-group">
          <label>Survey Plan ID * (must be approved)</label>
          <input v-model="form.survey_plan_id" required placeholder="UUID of approved survey plan" />
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="form.description"></textarea>
        </div>
        <div class="form-group">
          <label>Area (m²)</label>
          <input v-model.number="form.area_sqm" type="number" step="0.01" />
        </div>
        <div class="form-group">
          <label>Land Use</label>
          <input v-model="form.land_use" placeholder="e.g. residential, agricultural" />
        </div>
        <div class="form-group">
          <label>Geometry (WKT or GeoJSON)</label>
          <textarea v-model="form.geometry" placeholder="POLYGON((...))"></textarea>
        </div>
        <button class="btn btn-primary" :disabled="loading" type="submit">
          {{ loading ? 'Creating…' : 'Create Parcel' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { parcelsApi } from '../../api/index.js'

const router  = useRouter()
const loading = ref(false)
const error   = ref(null)
const success = ref(false)
const form    = ref({
  parcel_identifier: '',
  survey_plan_id: '',
  description: '',
  area_sqm: null,
  land_use: '',
  geometry: '',
})

async function submit() {
  error.value   = null
  success.value = false
  loading.value = true
  try {
    const res = await parcelsApi.create(form.value)
    success.value = true
    setTimeout(() => router.push(`/parcels/${res.data.id}`), 800)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to create parcel'
  } finally {
    loading.value = false
  }
}
</script>
