<script setup lang="ts">
import { ref } from 'vue'
import UploadFile from '../components/UploadFile.vue'
import ShowWave from '../components/ShowWave.vue'
import type { FileRecord } from '../types'
const extraData = ref({
  reverberance: 50.0,
  damping: 50.0,
  room_scale: 100.0,
  stereo_depth: 100.0,
  pre_delay: 0.0,
  wet_gain: 0.0,
  wet_only: false
})
const input = ref<FileRecord>()
const output = ref<FileRecord>()
</script>

<template>
  <el-main>
    <el-row>
      <span>Reverberance</span>
      <el-slider v-model="extraData.reverberance" :show-input="true" />
    </el-row>
    <el-row>
      <span>Damping</span>
      <el-slider v-model="extraData.damping" :show-input="true" />
    </el-row>
    <el-row>
      <span>Room Scale</span>
      <el-slider v-model="extraData.room_scale" :show-input="true" />
    </el-row>
    <el-row>
      <span>Stereo Depth</span>
      <el-slider v-model="extraData.stereo_depth" :show-input="true" />
    </el-row>
    <el-row>
      <span>Predelay</span>
      <el-slider v-model="extraData.pre_delay" :show-input="true" :max="500" />
    </el-row>
    <el-row>
      <span>Wet Gain</span>
      <el-slider
        v-model="extraData.wet_gain"
        :show-input="true"
        :min="-10"
        :max="10"
        :step="0.01"
      />
    </el-row>
    <el-row> Wet Only </el-row>
    <el-row>
      <el-radio-group v-model="extraData.wet_only" size="large" style="margin-top: 10px">
        <el-radio-button label="True" :value="true" />
        <el-radio-button label="False" :value="false" />
      </el-radio-group>
    </el-row>
    <ShowWave v-model="input" />
    <ShowWave v-model="output" />
  </el-main>
  <el-footer height="200px">
    <UploadFile
      :action="'http://localhost:8000/reverb/advanced/'"
      :extraData="extraData"
      v-model:input="input"
      v-model:output="output"
    />
  </el-footer>
</template>
