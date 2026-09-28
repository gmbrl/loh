<template>
  <div class="login-wrap">
    <div class="login-card">
      <h1>Land &amp; Cadastral Registry</h1>
      <p>Sign in to your authority account</p>

      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required autocomplete="current-password" />
        </div>
        <button class="btn btn-primary" style="width:100%" :disabled="loading" type="submit">
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth   = useAuthStore()
const router = useRouter()
const route  = useRoute()

const email    = ref('')
const password = ref('')
const loading  = ref(false)
const error    = ref(null)

async function submit() {
  error.value   = null
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push(route.query.redirect || '/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
