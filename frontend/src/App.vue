<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import { useDark, useToggle } from '@vueuse/core'

const preset = ref('default')
const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<template>
  <el-container>
    <el-aside width="200px">
      <el-row align="middle" justify="center">
        <el-col :span="6" :offset="1">
          <img src="@/assets/logo.svg" />
        </el-col>
        <el-col :span="13">
          <el-text type="primary" style="font-size: var(--el-font-size-extra-large);">
            数字混响师
          </el-text>
        </el-col>
        <el-col :span="4" @click="toggleDark()">
          <template v-if="isDark">
            <el-icon :size="25">
              <Moon />
            </el-icon>
          </template>
          <template v-else>
            <el-icon :size="25">
              <Sunny />
            </el-icon>
          </template>
        </el-col>
      </el-row>
      <el-menu default-active="default" :router=true>
        <el-menu-item index="default" :route="{ path: '/' }" @click="preset = 'default'">
          <el-icon>
            <User />
          </el-icon>
          <span>Default 默认</span>
        </el-menu-item>
        <el-menu-item index="advanced" :route="{ path: '/advanced' }">
          <el-icon>
            <Operation />
          </el-icon>
          <span>Advanced 高级</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container direction="vertical">
      <RouterView v-model="preset" />
    </el-container>
  </el-container>
</template>

<style scoped>
.el-icon {
  cursor: pointer;
  margin: 10%;
}

.el-menu {
  padding: 10px 10px;
}

.el-menu-item {
  border-radius: 10px;
}
</style>