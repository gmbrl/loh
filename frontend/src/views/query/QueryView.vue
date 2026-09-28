<template>
  <div>
    <div class="page-header">
      <h1>Search Land Records</h1>
    </div>

    <!-- Parcel search -->
    <div class="card">
      <h2>Parcels</h2>
      <div class="flex gap-2 items-center">
        <input v-model="parcelQ.identifier" placeholder="Identifier" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px" />
        <input v-model="parcelQ.land_use" placeholder="Land Use" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px" />
        <button class="btn btn-primary" @click="searchParcels">Search</button>
      </div>
      <table v-if="parcels.length" class="data-table mt-2">
        <thead><tr><th>Identifier</th><th>Area (m²)</th><th>Land Use</th><th>Status</th><th></th></tr></thead>
        <tbody>
          <tr v-for="p in parcels" :key="p.id">
            <td>{{ p.parcel_identifier }}</td>
            <td>{{ p.area_sqm?.toLocaleString() || '—' }}</td>
            <td>{{ p.land_use || '—' }}</td>
            <td><StatusBadge :status="p.status" /></td>
            <td><router-link :to="`/parcels/${p.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="parcelSearched" class="empty">No parcels found.</p>
    </div>

    <!-- Title search -->
    <div class="card">
      <h2>Titles</h2>
      <div class="flex gap-2 items-center">
        <input v-model="titleQ.title_number" placeholder="Title number" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px" />
        <input v-model="titleQ.parcel_id" placeholder="Parcel ID" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px" />
        <button class="btn btn-primary" @click="searchTitles">Search</button>
      </div>
      <table v-if="titles.length" class="data-table mt-2">
        <thead><tr><th>Title No.</th><th>Owner</th><th>Status</th><th></th></tr></thead>
        <tbody>
          <tr v-for="t in titles" :key="t.id">
            <td>{{ t.title_number }}</td>
            <td>{{ t.owner_name }}</td>
            <td><StatusBadge :status="t.status" /></td>
            <td><router-link :to="`/titles/${t.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="titleSearched" class="empty">No titles found.</p>
    </div>

    <!-- Encumbrance search -->
    <div class="card">
      <h2>Encumbrances</h2>
      <div class="flex gap-2 items-center">
        <input v-model="encQ.title_id" placeholder="Title ID" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px" />
        <input v-model="encQ.parcel_id" placeholder="Parcel ID" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px" />
        <select v-model="encQ.enc_type" style="flex:1;padding:7px 10px;border:1px solid #d1d5db;border-radius:5px;font-size:13px">
          <option value="">All types</option>
          <option value="mortgage">Mortgage</option>
          <option value="tax_lien">Tax Lien</option>
          <option value="court_seizure">Court Seizure</option>
          <option value="municipal_restriction">Municipal Restriction</option>
          <option value="easement">Easement</option>
        </select>
        <button class="btn btn-primary" @click="searchEnc">Search</button>
      </div>
      <table v-if="encs.length" class="data-table mt-2">
        <thead><tr><th>Type</th><th>Authority</th><th>Status</th><th></th></tr></thead>
        <tbody>
          <tr v-for="e in encs" :key="e.id">
            <td>{{ e.encumbrance_type }}</td>
            <td>{{ e.originating_authority || '—' }}</td>
            <td><StatusBadge :status="e.status" /></td>
            <td><router-link :to="`/encumbrances/${e.id}`" class="btn btn-ghost">View</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="encSearched" class="empty">No encumbrances found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { queryApi } from '../../api/index.js'
import StatusBadge from '../../components/StatusBadge.vue'

const parcels       = ref([])
const parcelQ       = ref({ identifier: '', land_use: '' })
const parcelSearched = ref(false)

const titles        = ref([])
const titleQ        = ref({ title_number: '', parcel_id: '' })
const titleSearched = ref(false)

const encs          = ref([])
const encQ          = ref({ title_id: '', parcel_id: '', enc_type: '' })
const encSearched   = ref(false)

async function searchParcels() {
  const p = {}
  if (parcelQ.value.identifier) p.identifier = parcelQ.value.identifier
  if (parcelQ.value.land_use)   p.land_use   = parcelQ.value.land_use
  parcels.value = (await queryApi.parcels(p)).data
  parcelSearched.value = true
}

async function searchTitles() {
  const p = {}
  if (titleQ.value.title_number) p.title_number = titleQ.value.title_number
  if (titleQ.value.parcel_id)    p.parcel_id    = titleQ.value.parcel_id
  titles.value = (await queryApi.titles(p)).data
  titleSearched.value = true
}

async function searchEnc() {
  const p = {}
  if (encQ.value.title_id)  p.title_id  = encQ.value.title_id
  if (encQ.value.parcel_id) p.parcel_id = encQ.value.parcel_id
  if (encQ.value.enc_type)  p.enc_type  = encQ.value.enc_type
  encs.value = (await queryApi.encumbrances(p)).data
  encSearched.value = true
}
</script>
