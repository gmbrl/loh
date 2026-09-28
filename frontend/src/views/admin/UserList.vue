<template>
  <div>
    <div class="page-header">
      <h1>Manage Users</h1>
      <button class="btn btn-primary" @click="showForm = !showForm">+ New User</button>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="createSuccess" class="alert alert-success">User created.</div>

    <div v-if="showForm" class="card">
      <h2>Create User</h2>
      <form @submit.prevent="createUser">
        <div class="form-group">
          <label>Email *</label>
          <input v-model="form.email" type="email" required />
        </div>
        <div class="form-group">
          <label>Full Name *</label>
          <input v-model="form.full_name" required />
        </div>
        <div class="form-group">
          <label>Password *</label>
          <input v-model="form.password" type="password" required />
        </div>
        <div class="form-group">
          <label>Role *</label>
          <select v-model="form.role" required>
            <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>
        <button class="btn btn-primary" :disabled="creating" type="submit">
          {{ creating ? 'Creating…' : 'Create User' }}
        </button>
      </form>
    </div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr><th>Email</th><th>Name</th><th>Role</th><th>Active</th><th>Created</th></tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.email }}</td>
            <td>{{ u.full_name }}</td>
            <td>{{ u.role }}</td>
            <td>{{ u.is_active ? '✓' : '✗' }}</td>
            <td>{{ fmtDate(u.created_at) }}</td>
          </tr>
          <tr v-if="!users.length">
            <td colspan="5" class="empty">No users.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usersApi } from '../../api/index.js'

const users         = ref([])
const error         = ref(null)
const showForm      = ref(false)
const creating      = ref(false)
const createSuccess = ref(false)
const form          = ref({ email: '', full_name: '', password: '', role: 'citizen' })

const roles = [
  'admin', 'surveyor', 'cadastral_officer', 'lawyer_notary',
  'registrar', 'bank', 'tax_authority', 'court', 'municipality', 'citizen',
]

onMounted(async () => {
  try { users.value = (await usersApi.list()).data }
  catch (e) { error.value = e.response?.data?.detail || 'Failed to load users' }
})

async function createUser() {
  creating.value      = true
  error.value         = null
  createSuccess.value = false
  try {
    const res = await usersApi.create(form.value)
    users.value.push(res.data)
    createSuccess.value = true
    showForm.value = false
    form.value = { email: '', full_name: '', password: '', role: 'citizen' }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to create user'
  } finally {
    creating.value = false
  }
}

const fmtDate = (d) => d ? new Date(d).toLocaleDateString() : '—'
</script>
