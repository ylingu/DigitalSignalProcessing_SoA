<script setup lang="ts">
import { defineProps } from 'vue';

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
async function customRequest(options: any, uploadConfig: UploadConfig) {
  const { file, onSuccess, onError } = options;
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
      onSuccess({ message: 'File downloaded successfully.' });
    } else {
      onError({ status: response.status });
    }
  } catch (error) {
    onError({ error });
  }
}
</script>

<template>
  <main>
    <el-upload class="upload-demo" :http-request="(options: any) => customRequest(options, props.uploadConfig)">
      <template #trigger>
        <el-button type="primary">选取音频文件</el-button>
      </template>
    </el-upload>
  </main>
</template>