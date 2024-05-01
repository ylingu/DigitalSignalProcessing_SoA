<script setup lang="ts">
import { ref } from 'vue'
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
interface UploadConfig {
  action: string;
  extraData: Record<string, number | boolean> | string;
}
const props = defineProps({
  uploadConfig: {
    type: Object as () => UploadConfig,
    required: true
  }
});
const result = ref({
  show: false,
  icon: 'success'
});
const isLoading = ref(false);
function setback() {
  isLoading.value = false;
  result.value.show = false;
  result.value.icon = 'success';
}
function handleUploadError() {
  isLoading.value = false;
  result.value.icon = 'error';
  result.value.show = true;
}
async function customRequest(options: any, uploadConfig: UploadConfig) {
  isLoading.value = true;
  const { file, onError } = options;
  const formData = new FormData();

  formData.append('file', file);
  if (typeof uploadConfig.extraData === 'object') {
    const extraDataJson = JSON.stringify(uploadConfig.extraData);
    formData.append('settings', extraDataJson);
  } else if (typeof uploadConfig.extraData === 'string') {
    formData.append('preset', uploadConfig.extraData);
  }


  try {
    const response = await fetch(uploadConfig.action, {
      method: 'POST',
      body: formData,
    });
    if (response.ok) {
      isLoading.value = false;
      result.value.show = true;
      setTimeout(() => {
        result.value.show = false;
      }, 1000);
      // 处理文件下载
      const blob = await response.blob(); // 获取二进制数据
      const downloadUrl = window.URL.createObjectURL(blob); // 创建下载链接
      const a = document.createElement('a');
      a.href = downloadUrl; // 设置下载链接
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'downloaded_file';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch && filenameMatch.length === 2) {
          filename = filenameMatch[1];
        }
      }
      a.download = filename; // 设置下载文件名
      document.body.appendChild(a); // 附加元素到DOM以支持下载
      a.click(); // 触发下载
      window.URL.revokeObjectURL(downloadUrl); // 清理下载链接
      a.remove(); // 清理创建的元素
    } else {
      onError(handleUploadError());
    }
  } catch (error) {
    onError(handleUploadError());
  }
}
</script>

<template>
  <el-result v-if=result.show :icon=result.icon>
    <template #extra>
      <el-button type="primary" @click="setback()">Back</el-button>
    </template>
  </el-result>
  <el-upload :http-request="(options: any) => customRequest(options, props.uploadConfig)" :show-file-list="false" drag
    v-loading=isLoading element-loading-text="处理中..." :element-loading-spinner="svg"
    element-loading-svg-view-box="-10, -10, 50, 50" v-else>
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
  </el-upload>
</template>