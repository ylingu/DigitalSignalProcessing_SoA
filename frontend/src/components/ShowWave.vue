<script setup lang="ts">
import { onMounted, watch } from 'vue'
import WaveSurfer from 'wavesurfer.js'
import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram.esm.js'
import Timeline from 'wavesurfer.js/dist/plugins/timeline.esm.js'
import ZoomPlugin from 'wavesurfer.js/dist/plugins/zoom.esm.js'
import type { FileRecord } from '../types'
const url = defineModel<FileRecord>({ default: { filename: '', url: '' } })
let ws: WaveSurfer
let spectrogram: Spectrogram
onMounted(() => {
  ws = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#409eff',
    progressColor: '#337ecc',
    cursorWidth: 2,
    autoCenter: true,
    autoScroll: true,
    dragToSeek: true
  })
  ws.once('ready', () => {
    ws.registerPlugin(
      ZoomPlugin.create({
        scale: 0.1,
        maxZoom: 100
      })
    )
    ws.registerPlugin(Timeline.create())
  })
  ws.on('ready', () => {
    if (spectrogram) spectrogram.destroy()
    spectrogram = Spectrogram.create({
      labels: true,
      height: 125
    })
    ws.registerPlugin(spectrogram)
    ws.zoom(0)
  })
  ws.on('click', () => {
    ws.playPause()
  })
  ws.on('dblclick', async () => {
    const a = document.createElement('a')
    a.href = url.value.url // 设置下载链接
    a.download = url.value.filename // 设置下载文件名
    document.body.appendChild(a) // 附加元素到DOM以支持下载
    a.click() // 触发下载
    a.remove() // 清理创建的元素
  })
})
watch(url, (newValue: FileRecord, oldValue: FileRecord) => {
  ws.load(newValue.url)
  window.URL.revokeObjectURL(oldValue.url)
})
</script>

<template>
  <div id="waveform"></div>
</template>
