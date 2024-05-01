<script setup lang="ts">
import UploadFile from '../components/UploadFile.vue'
const preset = defineModel({
  type: String,
  required: true
})
</script>

<template>
  <el-main>
    <el-image src='https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg' fit="cover" />
  </el-main>
  <el-footer height="200px">
    <UploadFile :uploadConfig="{ action: 'http://localhost:8000/reverb/', extraData: preset }" />
  </el-footer>
</template>

<style scoped>
.el-image {
  width: 100%;
  height: 99%;
}
</style>