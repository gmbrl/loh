<template>
  <div>
    <div class="page-header">
      <h1>Encumbrance Detail</h1>
      <router-link to="/encumbrances" class="btn btn-ghost">← Back</router-link>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="actionSuccess" class="alert alert-success">{{ actionMsg }}</div>

    <div v-if="item" class="card">
      <h2>{{ item.encumbrance_type }}</h2>
      <table class="data-table mt-2">
        <tbody>
          <tr><td><strong>Status</strong></td><td><StatusBadge :status="item.status" /></td></tr>
          <tr><td><strong>Title</strong></td><td>
            <router-link v-if="item.title_id" :to="`/titles/${item.title_id}`">{{ item.title_id }}</router-link>
            <span v-else>—</span>
          </td></tr>
          <tr><td><strong>Parcel</strong></td><td>
            <router-link v-if="item.parcel_id" :to="`/parcels/${item.parcel_id}`">{{ item.parcel_id }}</router-link>
            <span v-else>—</span>
          </td></tr>
          <tr><td><strong>Originating Authority</strong></td><td>{{ item.originating_authority || '—' }}</td></tr>
          <tr><td><strong>Instrument Reference</strong></td><td>{{ item.instrument_reference || '—' }}</td></tr>
          <tr><td><strong>Description</strong></td><td>{{ item.description || '—' }}</td></tr>
          <tr><td><strong>Submitted</strong></td><td>{{ fmtDate(item.submitted_at) }}</td></tr>
          <tr><td><strong>Approved</strong></td><td>{{ fmtDate(item.approved_at) }}</td></tr>
          <tr><td><strong>Released</strong></td><td>{{ fmtDate(item.released_at) }}</td></tr>
          <tr><td><strong>Release Reference</strong></td><td>{{ item.release_reference || '—' }}</td></tr>
        </tbody>
      </table>

      <!-- Approve -->
      <div v-if="item.status === 'pending' && (auth.isRegistrar || auth.isAdmin)" class="mt-3">
        <button class="btn btn-success" :disabled="acting" @click="approve">Approve &amp; Activate</button>
      </div>

      <!-- Release -->
      <div v-if="item.status === 'active' && canRelease" class="mt-3">
        <h3>Release Encumbrance</h3>
        <div class="form-group mt-1">
          <label>Release Reference *</label>
          <input v-model="releaseRef" placeholder="Discharge order, settlement ref, etc." />
        </div>
        <button class="btn btn-danger" :disabled="acting || !releaseRef" @click="release">Release</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { encumbrancesApi } from '../../api/index.js'
import { useAuthStore } from '../../stores/auth.js'
import StatusBadge from '../../components/StatusBadge.vue'

const route         = useRoute()
const auth          = useAuthStore()
const item          = ref(null)
const error         = ref(null)
const releaseRef    = ref('')
const acting        = ref(false)
const actionSuccess = ref(false)
const actionMsg     = ref('')

const canRelease = computed(() =>
  auth.isBank || auth.isTaxAuthority || auth.isCourt || auth.isMunicipality ||
  auth.isRegistrar || auth.isAdmin
)

onMounted(async () => {
  try { item.value = (await encumbrancesApi.get(route.params.id)).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load encumbrance' }
})

async function approve() {
  acting.value = true; error.value = null
  try {
    item.value = (await encumbrancesApi.approve(route.params.id)).data
    actionMsg.value = 'Encumbrance activated.'
    actionSuccess.value = true
  } catch (e) { error.value = e.response?.data?.detail || 'Approve failed' }
  finally { acting.value = false }
}

async function release() {
  acting.value = true; error.value = null
  try {
    item.value = (await encumbrancesApi.release(route.params.id, { release_reference: releaseRef.value })).data
    actionMsg.value = 'Encumbrance released.'
    actionSuccess.value = true
  } catch (e) { error.value = e.response?.data?.detail || 'Release failed' }
  finally { acting.value = false }
}

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
