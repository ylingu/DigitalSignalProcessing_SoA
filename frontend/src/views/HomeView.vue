<script setup lang="ts">
import { ref, inject } from 'vue'
import type { Ref } from 'vue'
import { key } from '../keys'
import UploadFile from '../components/UploadFile.vue'
import ShowWave from '../components/ShowWave.vue'
import type { FileRecord } from '../types'
const preset = inject<Ref<string>>(key)
const input = ref<FileRecord>()
const output = ref<FileRecord>()
</script>

<template>
  <el-main>
    <ShowWave v-model="input" />
    <ShowWave v-model="output" />
  </el-main>
  <el-footer height="200px">
    <UploadFile
      :action="'http://localhost:8000/reverb/'"
      :extraData="preset"
      v-model:input="input"
      v-model:output="output"
    />
  </el-footer>
</template>
