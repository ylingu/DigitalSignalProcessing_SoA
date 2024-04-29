<script setup lang="ts">
import { ref } from 'vue'
import UploadFile from '../components/UploadFile.vue'
const extraData = ref({
  reverberance: 50.0,
  damping: 50.0,
  room_scale: 100.0,
  stereo_depth: 100.0,
  pre_delay: 0.0,
  wet_gain: 0.0,
  wet_only: false,
})
</script>

<template>
  <main>
    <div>
      <span>Reverberance</span>
      <el-slider v-model="extraData.reverberance" :show-input=true />
    </div>
    <div>
      <span>Damping</span>
      <el-slider v-model="extraData.damping" :show-input=true />
    </div>
    <div>
      <span>Room Scale</span>
      <el-slider v-model="extraData.room_scale" :show-input=true />
    </div>
    <div>
      <span>Stereo Depth</span>
      <el-slider v-model="extraData.stereo_depth" :show-input=true />
    </div>
    <div>
      <span>Predelay</span>
      <el-slider v-model="extraData.pre_delay" :show-input=true :max="500" />
    </div>
    <div>
      <span>Wet Gain</span>
      <el-slider v-model="extraData.wet_gain" :show-input=true :min="-10" :max="10" :step="0.01" />
    </div>
    <el-col :span="3" style="margin-bottom: 20px;">
      <span>Wet Only</span>
      <el-radio-group v-model="extraData.wet_only" size="large" style="margin-top: 10px;">
        <el-radio-button label="True" :value="true" />
        <el-radio-button label="False" :value="false" />
      </el-radio-group>
    </el-col>
  </main>
  <UploadFile :uploadConfig="{ action: 'http://localhost:8000/reverb/advanced/', extraData: extraData }" />
</template>