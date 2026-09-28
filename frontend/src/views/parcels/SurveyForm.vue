<template>
  <div>
    <div class="page-header">
      <h1>Submit Survey Plan</h1>
      <router-link to="/parcels/surveys" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="success" class="alert alert-success">Survey plan submitted.</div>

    <div class="card">
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Reference Number *</label>
          <input v-model="form.reference_number" required />
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
          <label>Geometry (WKT or GeoJSON)</label>
          <textarea v-model="form.geometry" placeholder="POLYGON((...))"></textarea>
        </div>
        <button class="btn btn-primary" :disabled="loading" type="submit">
          {{ loading ? 'Submitting…' : 'Submit Survey Plan' }}
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
const form    = ref({ reference_number: '', description: '', area_sqm: null, geometry: '' })

async function submit() {
  error.value   = null
  success.value = false
  loading.value = true
  try {
    const res = await parcelsApi.submitSurvey(form.value)
    success.value = true
    setTimeout(() => router.push(`/parcels/surveys/${res.data.id}`), 800)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to submit survey'
  } finally {
    loading.value = false
  }
}
</script>
