<template>
  <div>
    <div class="page-header">
      <h1>Application Detail</h1>
      <router-link to="/titles/applications" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="decisionSuccess" class="alert alert-success">Decision saved.</div>

    <div v-if="app" class="card">
      <h2>{{ app.instrument_type }} — {{ app.proposed_owner_name }}</h2>
      <table class="data-table mt-2">
        <tbody>
          <tr><td><strong>Parcel</strong></td><td>
            <router-link :to="`/parcels/${app.parcel_id}`">{{ app.parcel_id }}</router-link>
          </td></tr>
          <tr><td><strong>Status</strong></td><td><StatusBadge :status="app.status" /></td></tr>
          <tr><td><strong>Instrument Description</strong></td><td>{{ app.instrument_description || '—' }}</td></tr>
          <tr><td><strong>Proposed Owner ID</strong></td><td>{{ app.proposed_owner_id_ref || '—' }}</td></tr>
          <tr><td><strong>Submitted</strong></td><td>{{ fmtDate(app.submitted_at) }}</td></tr>
          <tr><td><strong>Decided</strong></td><td>{{ fmtDate(app.decided_at) }}</td></tr>
          <tr><td><strong>Registrar Notes</strong></td><td>{{ app.registrar_notes || '—' }}</td></tr>
        </tbody>
      </table>

      <!-- Registrar decision panel -->
      <div v-if="app.status !== 'approved' && app.status !== 'rejected' && (auth.isRegistrar || auth.isAdmin)" class="mt-3">
        <h3>Registrar Decision</h3>
        <div class="form-group mt-1">
          <label>Notes</label>
          <textarea v-model="notes"></textarea>
        </div>
        <div class="form-group">
          <label>Title Number (required when approving)</label>
          <input v-model="titleNumber" placeholder="e.g. T-2024-0001" />
        </div>
        <div class="flex gap-2 mt-1">
          <button class="btn btn-primary" :disabled="deciding" @click="decide('under_review')">Mark Under Review</button>
          <button class="btn btn-success"  :disabled="deciding" @click="decide('approved')">Approve &amp; Register</button>
          <button class="btn btn-danger"   :disabled="deciding" @click="decide('rejected')">Reject</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { titlesApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const route          = useRoute()
const auth           = useAuthStore()
const app            = ref(null)
const error          = ref(null)
const notes          = ref('')
const titleNumber    = ref('')
const deciding       = ref(false)
const decisionSuccess = ref(false)

onMounted(async () => {
  try { app.value = (await titlesApi.getApplication(route.params.id)).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load application' }
})

async function decide(status) {
  error.value          = null
  decisionSuccess.value = false
  deciding.value        = true
  try {
    app.value            = (await titlesApi.decideApplication(route.params.id, {
      status,
      registrar_notes: notes.value,
      title_number: status === 'approved' ? titleNumber.value : undefined,
    })).data
    decisionSuccess.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Decision failed'
  } finally {
    deciding.value = false
  }
}

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
