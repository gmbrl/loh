<template>
  <div>
    <div class="page-header">
      <h1>Survey Plan Detail</h1>
      <router-link to="/parcels/surveys" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="reviewSuccess" class="alert alert-success">Review decision saved.</div>

    <div v-if="plan" class="card">
      <h2>{{ plan.reference_number }}</h2>
      <table class="data-table mt-2">
        <tbody>
          <tr><td><strong>ID</strong></td><td>{{ plan.id }}</td></tr>
          <tr><td><strong>Status</strong></td><td><StatusBadge :status="plan.status" /></td></tr>
          <tr><td><strong>Area (m²)</strong></td><td>{{ plan.area_sqm?.toLocaleString() || '—' }}</td></tr>
          <tr><td><strong>Description</strong></td><td>{{ plan.description || '—' }}</td></tr>
          <tr><td><strong>Submitted</strong></td><td>{{ fmtDate(plan.submitted_at) }}</td></tr>
          <tr><td><strong>Reviewed</strong></td><td>{{ fmtDate(plan.reviewed_at) }}</td></tr>
          <tr><td><strong>Review Notes</strong></td><td>{{ plan.review_notes || '—' }}</td></tr>
          <tr><td><strong>Geometry</strong></td><td><code style="font-size:11px">{{ plan.geometry || '—' }}</code></td></tr>
        </tbody>
      </table>

      <!-- Cadastral officer review panel -->
      <div v-if="plan.status === 'pending' && (auth.isCadastral || auth.isAdmin)" class="mt-3">
        <h3>Review Decision</h3>
        <div class="form-group mt-1">
          <label>Notes</label>
          <textarea v-model="reviewNotes"></textarea>
        </div>
        <div class="flex gap-2 mt-1">
          <button class="btn btn-success" :disabled="reviewing" @click="review('approved')">Approve</button>
          <button class="btn btn-danger"  :disabled="reviewing" @click="review('rejected')">Reject</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { parcelsApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const route         = useRoute()
const auth          = useAuthStore()
const plan          = ref(null)
const error         = ref(null)
const reviewNotes   = ref('')
const reviewing     = ref(false)
const reviewSuccess = ref(false)

onMounted(async () => {
  try { plan.value = (await parcelsApi.getSurvey(route.params.id)).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load survey plan' }
})

async function review(status) {
  reviewing.value = true
  error.value     = null
  try {
    plan.value      = (await parcelsApi.reviewSurvey(route.params.id, { status, review_notes: reviewNotes.value })).data
    reviewSuccess.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Review failed'
  } finally {
    reviewing.value = false
  }
}

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
