<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import { useDark, useToggle } from '@vueuse/core'

const preset = ref('auto')
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
      <el-menu :default-active=preset :router=true>
        <el-menu-item index="auto" :route="{ path: '/' }" @click="preset = 'auto'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#bell" />
            </svg>
          </el-icon>
          <span>Auto 自动选择</span>
        </el-menu-item>
        <el-menu-item index="blues" :route="{ path: '/' }" @click="preset = 'blues'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#guitar" />
            </svg>
          </el-icon>
          <span>Blues 蓝调</span>
        </el-menu-item>
        <el-menu-item index="classical" :route="{ path: '/' }" @click="preset = 'classical'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#violin" />
            </svg>
          </el-icon>
          <span>Classical 古典</span>
        </el-menu-item>
        <el-menu-item index="country" :route="{ path: '/' }" @click="preset = 'country'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#drum" />
            </svg>
          </el-icon>
          <span>Country 乡村</span>
        </el-menu-item>
        <el-menu-item index="disco" :route="{ path: '/' }" @click="preset = 'disco'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#disco" />
            </svg>
          </el-icon>
          <span>Disco 迪斯科</span>
        </el-menu-item>
        <el-menu-item index="hiphop" :route="{ path: '/' }" @click="preset = 'hiphop'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#zils" />
            </svg>
          </el-icon>
          <span>Hiphop 嘻哈</span>
        </el-menu-item>
        <el-menu-item index="jazz" :route="{ path: '/' }" @click="preset = 'jazz'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#keyboard" />
            </svg>
          </el-icon>
          <span>Jazz 爵士</span>
        </el-menu-item>
        <el-menu-item index="metal" :route="{ path: '/' }" @click="preset = 'metal'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#electric-guitar" />
            </svg>
          </el-icon>
          <span>Metal 重金属</span>
        </el-menu-item>
        <el-menu-item index="pop" :route="{ path: '/' }" @click="preset = 'pop'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#triangle" />
            </svg>
          </el-icon>
          <span>Pop 流行</span>
        </el-menu-item>
        <el-menu-item index="reggae" :route="{ path: '/' }" @click="preset = 'reggae'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#drum1" />
            </svg>
          </el-icon>
          <span>Reggae 雷鬼</span>
        </el-menu-item>
        <el-menu-item index="rock" :route="{ path: '/' }" @click="preset = 'rock'">
          <el-icon :size="25">
            <svg>
              <use href="@/assets/icons.svg#shakers" />
            </svg>
          </el-icon>
          <span>Rock 摇滚</span>
        </el-menu-item>
        <el-menu-item index="advanced" :route="{ path: '/advanced' }">
          <el-icon>
            <svg>
              <use href="@/assets/icons.svg#settings" />
            </svg>
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