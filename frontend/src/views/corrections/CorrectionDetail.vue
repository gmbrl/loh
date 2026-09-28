<template>
  <div>
    <div class="page-header">
      <h1>Correction Request Detail</h1>
      <router-link to="/corrections" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="reviewSuccess" class="alert alert-success">Review decision saved.</div>

    <div v-if="item" class="card">
      <h2>{{ item.correction_level }} correction</h2>
      <table class="data-table mt-2">
        <tbody>
          <tr><td><strong>Status</strong></td><td><StatusBadge :status="item.status" /></td></tr>
          <tr><td><strong>Parcel</strong></td><td>
            <router-link v-if="item.parcel_id" :to="`/parcels/${item.parcel_id}`">{{ item.parcel_id }}</router-link>
            <span v-else>—</span>
          </td></tr>
          <tr><td><strong>Title</strong></td><td>
            <router-link v-if="item.title_id" :to="`/titles/${item.title_id}`">{{ item.title_id }}</router-link>
            <span v-else>—</span>
          </td></tr>
          <tr><td><strong>Description</strong></td><td>{{ item.description }}</td></tr>
          <tr><td><strong>Evidence</strong></td><td>{{ item.evidence_reference || '—' }}</td></tr>
          <tr><td><strong>Submitted</strong></td><td>{{ fmtDate(item.submitted_at) }}</td></tr>
          <tr><td><strong>Reviewed</strong></td><td>{{ fmtDate(item.reviewed_at) }}</td></tr>
          <tr><td><strong>Review Notes</strong></td><td>{{ item.review_notes || '—' }}</td></tr>
        </tbody>
      </table>

      <!-- Review panel -->
      <div v-if="item.status !== 'approved' && item.status !== 'rejected' && (auth.isCadastral || auth.isRegistrar || auth.isAdmin)" class="mt-3">
        <h3>Review Decision</h3>
        <div class="form-group mt-1">
          <label>Notes</label>
          <textarea v-model="notes"></textarea>
        </div>
        <div class="flex gap-2 mt-1">
          <button class="btn btn-primary" :disabled="reviewing" @click="review('under_review')">Mark Under Review</button>
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
import { correctionsApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const route         = useRoute()
const auth          = useAuthStore()
const item          = ref(null)
const error         = ref(null)
const notes         = ref('')
const reviewing     = ref(false)
const reviewSuccess = ref(false)

onMounted(async () => {
  try { item.value = (await correctionsApi.get(route.params.id)).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load correction' }
})

async function review(status) {
  reviewing.value = true; error.value = null
  try {
    item.value = (await correctionsApi.review(route.params.id, { status, review_notes: notes.value })).data
    reviewSuccess.value = true
  } catch (e) { error.value = e.response?.data?.detail || 'Review failed' }
  finally { reviewing.value = false }
}

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
