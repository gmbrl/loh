<template>
  <div>
    <div class="page-header">
      <h1>New Correction Request</h1>
      <router-link to="/corrections" class="btn btn-ghost">← Back</router-link>
    </div>

    <div class="alert alert-info">
      Clerical corrections can be made administratively. Technical corrections require a corrected survey.
      Substantive corrections require court order or consent of affected parties.
    </div>

    <div v-if="error" class="alert alert-error mt-2">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-2">Correction request submitted.</div>

    <div class="card mt-2">
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Correction Level *</label>
          <select v-model="form.correction_level" required>
            <option value="">— Select —</option>
            <option value="clerical">Clerical (spelling, typo, date, format)</option>
            <option value="technical">Technical (coordinates, area, boundary)</option>
            <option value="substantive">Substantive (ownership, priority, fraud)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Parcel ID (if parcel correction)</label>
          <input v-model="form.parcel_id" />
        </div>
        <div class="form-group">
          <label>Title ID (if title correction)</label>
          <input v-model="form.title_id" />
        </div>
        <div class="form-group">
          <label>Description *</label>
          <textarea v-model="form.description" required></textarea>
        </div>
        <div class="form-group">
          <label>Evidence Reference</label>
          <textarea v-model="form.evidence_reference" placeholder="Survey plan ref, court order no., consent doc, etc."></textarea>
        </div>
        <button class="btn btn-primary" :disabled="loading" type="submit">
          {{ loading ? 'Submitting…' : 'Submit Correction Request' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { correctionsApi } from '../../api/index.js'

const router  = useRouter()
const loading = ref(false)
const error   = ref(null)
const success = ref(false)
const form    = ref({
  correction_level: '',
  parcel_id: '',
  title_id: '',
  description: '',
  evidence_reference: '',
})

async function submit() {
  error.value   = null
  success.value = false
  loading.value = true
  const payload = { ...form.value }
  if (!payload.parcel_id) delete payload.parcel_id
  if (!payload.title_id)  delete payload.title_id
  try {
    const res = await correctionsApi.submit(payload)
    success.value = true
    setTimeout(() => router.push(`/corrections/${res.data.id}`), 800)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to submit correction'
  } finally {
    loading.value = false
  }
}
</script>
