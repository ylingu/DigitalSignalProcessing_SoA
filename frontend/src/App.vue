<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'

const preset = ref('default')
</script>

<template>
  <div>
    <el-container>
      <el-aside width="200px">
        <el-col>
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
        </el-col>
      </el-aside>
      <el-main>
        <RouterView v-model="preset" />
      </el-main>
    </el-container>
  </div>
</template>