<template>
  <div>
    <div class="page-header">
      <h1>Dashboard</h1>
    </div>

    <div class="card">
      <h2>Welcome, {{ auth.user?.full_name }}</h2>
      <p class="text-muted mt-1">
        You are signed in as <strong>{{ auth.role }}</strong>.
        Use the sidebar to navigate to your workspace.
      </p>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;">
      <router-link class="card" style="display:block;text-decoration:none;color:inherit" to="/parcels">
        <h3>Parcels</h3>
        <p class="text-muted">Official cadastral parcels</p>
      </router-link>
      <router-link class="card" style="display:block;text-decoration:none;color:inherit" to="/titles">
        <h3>Titles</h3>
        <p class="text-muted">Registered ownership records</p>
      </router-link>
      <router-link class="card" style="display:block;text-decoration:none;color:inherit" to="/encumbrances">
        <h3>Encumbrances</h3>
        <p class="text-muted">Mortgages, liens, orders</p>
      </router-link>
      <router-link class="card" style="display:block;text-decoration:none;color:inherit" to="/corrections">
        <h3>Corrections</h3>
        <p class="text-muted">Record correction requests</p>
      </router-link>
      <router-link class="card" style="display:block;text-decoration:none;color:inherit" to="/query">
        <h3>Search</h3>
        <p class="text-muted">Query land records</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth.js'
const auth = useAuthStore()
</script>
