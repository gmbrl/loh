<template>
  <router-view v-if="!isAuthenticated" />
  <div v-else class="layout">
    <aside class="sidebar">
      <div class="brand">
        🏛 Land Registry
        <div class="role-badge">{{ auth.role }}</div>
      </div>

      <nav>
        <router-link to="/dashboard">Dashboard</router-link>

        <div class="nav-section">Cadastral</div>
        <router-link to="/parcels">Parcels</router-link>
        <router-link to="/parcels/surveys">Survey Plans</router-link>
        <router-link v-if="auth.isSurveyor || auth.isAdmin" to="/parcels/surveys/new">+ Submit Survey</router-link>
        <router-link v-if="auth.isCadastral || auth.isAdmin" to="/parcels/new">+ Create Parcel</router-link>

        <div class="nav-section">Title Registry</div>
        <router-link to="/titles">Titles</router-link>
        <router-link to="/titles/applications">Applications</router-link>
        <router-link
          v-if="auth.isLawyerNotary || auth.isCitizen || auth.isAdmin"
          to="/titles/applications/new"
        >+ New Application</router-link>

        <div class="nav-section">Encumbrances</div>
        <router-link to="/encumbrances">Encumbrances</router-link>
        <router-link
          v-if="auth.isBank || auth.isTaxAuthority || auth.isCourt || auth.isMunicipality || auth.isLawyerNotary || auth.isCitizen || auth.isAdmin"
          to="/encumbrances/new"
        >+ Submit Encumbrance</router-link>

        <div class="nav-section">Corrections</div>
        <router-link to="/corrections">Corrections</router-link>
        <router-link
          v-if="auth.isSurveyor || auth.isCadastral || auth.isRegistrar || auth.isCourt || auth.isAdmin"
          to="/corrections/new"
        >+ New Correction</router-link>

        <div class="nav-section">Query</div>
        <router-link to="/query">Search Records</router-link>

        <div v-if="auth.isAdmin" class="nav-section">Admin</div>
        <router-link v-if="auth.isAdmin" to="/admin/users">Manage Users</router-link>
      </nav>

      <button class="logout-btn" @click="auth.logout(); $router.push('/login')">
        Sign out
      </button>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth.js'

const auth = useAuthStore()
const isAuthenticated = computed(() => auth.isAuthenticated)
</script>
