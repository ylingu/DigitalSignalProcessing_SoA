<script setup lang="ts">
import UploadFile from '../components/UploadFile.vue'
const preset = defineModel({
  type: String,
  required: true
})
</script>

<template>
  <main>
    <UploadFile :uploadConfig="{ action: 'http://localhost:8000/reverb/', extraData: preset }" />
  </main>
</template>
