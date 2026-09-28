<template>
  <div>
    <div class="page-header">
      <h1>Submit Encumbrance</h1>
      <router-link to="/encumbrances" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="success" class="alert alert-success">Encumbrance submitted for registration.</div>

    <div class="card">
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Encumbrance Type *</label>
          <select v-model="form.encumbrance_type" required>
            <option value="">— Select —</option>
            <option value="mortgage">Mortgage</option>
            <option value="tax_lien">Tax Lien</option>
            <option value="court_seizure">Court Seizure</option>
            <option value="judgment_lien">Judgment Lien</option>
            <option value="municipal_restriction">Municipal Restriction</option>
            <option value="public_right_of_way">Public Right-of-Way</option>
            <option value="lease">Lease</option>
            <option value="easement">Easement</option>
            <option value="adverse_claim">Adverse Claim</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Title ID (if title-level)</label>
          <input v-model="form.title_id" placeholder="UUID of registered title" />
        </div>
        <div class="form-group">
          <label>Parcel ID (if parcel-level)</label>
          <input v-model="form.parcel_id" placeholder="UUID of parcel" />
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="form.description"></textarea>
        </div>
        <div class="form-group">
          <label>Originating Authority</label>
          <input v-model="form.originating_authority" placeholder="e.g. First National Bank, Tax Authority" />
        </div>
        <div class="form-group">
          <label>Instrument Reference</label>
          <input v-model="form.instrument_reference" placeholder="Deed No., Court Order No., etc." />
        </div>
        <button class="btn btn-primary" :disabled="loading" type="submit">
          {{ loading ? 'Submitting…' : 'Submit' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { encumbrancesApi } from '../../api/index.js'

const router  = useRouter()
const loading = ref(false)
const error   = ref(null)
const success = ref(false)
const form    = ref({
  encumbrance_type: '',
  title_id: '',
  parcel_id: '',
  description: '',
  originating_authority: '',
  instrument_reference: '',
})

async function submit() {
  error.value   = null
  success.value = false
  loading.value = true
  const payload = { ...form.value }
  if (!payload.title_id)  delete payload.title_id
  if (!payload.parcel_id) delete payload.parcel_id
  try {
    const res = await encumbrancesApi.submit(payload)
    success.value = true
    setTimeout(() => router.push(`/encumbrances/${res.data.id}`), 800)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to submit encumbrance'
  } finally {
    loading.value = false
  }
}
</script>
