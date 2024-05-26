<script setup lang="ts">
import { ref } from 'vue'
import type { FileRecord, UploadConfig } from '../types'
const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `
let props = defineProps<UploadConfig>()
const input = defineModel<FileRecord>('input')
const output = defineModel<FileRecord>('output')
const result = ref({
  show: false,
  icon: 'success'
})
const isLoading = ref(false)
function setback() {
  isLoading.value = false
  result.value.show = false
  result.value.icon = 'success'
}
function handleUploadError() {
  isLoading.value = false
  result.value.icon = 'error'
  result.value.show = true
}
async function customRequest(options: any, uploadConfig: UploadConfig) {
  isLoading.value = true
  const { file, onError } = options
  const formData = new FormData()
  formData.append('file', file)
  if (typeof uploadConfig.extraData === 'object') {
    const extraDataJson = JSON.stringify(uploadConfig.extraData)
    formData.append('settings', extraDataJson)
  } else if (typeof uploadConfig.extraData === 'string') {
    formData.append('preset', uploadConfig.extraData)
  }
  let url = window.URL.createObjectURL(file)
  input.value = { filename: file.name, url: url }

  try {
    const response = await fetch(uploadConfig.action, {
      method: 'POST',
      body: formData
    })
    if (response.ok) {
      isLoading.value = false
      result.value.show = true
      setTimeout(() => {
        result.value.show = false
      }, 1000)
      const blob = await response.blob() // 获取二进制数据
      url = window.URL.createObjectURL(blob) // 创建Blob链接
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = 'downloaded_file'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/)
        if (filenameMatch && filenameMatch.length === 2) {
          filename = filenameMatch[1]
        }
      }
      output.value = { filename: filename, url: url }
    } else {
      onError(handleUploadError())
    }
  } catch (error) {
    onError(handleUploadError())
  }
}
</script>

<template>
  <el-result v-if="result.show" :icon="result.icon">
    <template #extra>
      <el-button type="primary" @click="setback()">Back</el-button>
    </template>
  </el-result>
  <el-upload
    :http-request="(options: any) => customRequest(options, props)"
    :show-file-list="false"
    drag
    v-loading="isLoading"
    element-loading-text="处理中..."
    :element-loading-spinner="svg"
    element-loading-svg-view-box="-10, -10, 50, 50"
    v-else
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
  </el-upload>
</template>
