<template>
  <div>
    <div class="page-header">
      <h1>New Title Application</h1>
      <router-link to="/titles/applications" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="success" class="alert alert-success">Application submitted.</div>

    <div class="card">
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Parcel ID *</label>
          <input v-model="form.parcel_id" required placeholder="UUID of active parcel" />
        </div>
        <div class="form-group">
          <label>Instrument Type *</label>
          <select v-model="form.instrument_type" required>
            <option value="">— Select —</option>
            <option value="first_registration">First Registration</option>
            <option value="transfer">Transfer</option>
            <option value="inheritance">Inheritance</option>
            <option value="court_order">Court Order</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Instrument Description</label>
          <textarea v-model="form.instrument_description"></textarea>
        </div>
        <div class="form-group">
          <label>Proposed Owner Name *</label>
          <input v-model="form.proposed_owner_name" required />
        </div>
        <div class="form-group">
          <label>Proposed Owner ID Reference</label>
          <input v-model="form.proposed_owner_id_ref" placeholder="National ID, passport, etc." />
        </div>
        <button class="btn btn-primary" :disabled="loading" type="submit">
          {{ loading ? 'Submitting…' : 'Submit Application' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { titlesApi } from '../../api/index.js'

const router  = useRouter()
const loading = ref(false)
const error   = ref(null)
const success = ref(false)
const form    = ref({
  parcel_id: '',
  instrument_type: '',
  instrument_description: '',
  proposed_owner_name: '',
  proposed_owner_id_ref: '',
})

async function submit() {
  error.value   = null
  success.value = false
  loading.value = true
  try {
    const res = await titlesApi.createApplication(form.value)
    success.value = true
    setTimeout(() => router.push(`/titles/applications/${res.data.id}`), 800)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to submit application'
  } finally {
    loading.value = false
  }
}
</script>
