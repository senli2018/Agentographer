<template>
  <el-menu
    class="side-menu"
    :default-active="activeMenuItem"
  >
    <template v-for="item in menuData" :key="item.index">
      <el-sub-menu :index="item.index">
        <template #title>
          <!-- <el-icon v-if="item.icon">
            <component :is="item.icon" />
          </el-icon> -->
          <span>{{ item.title }}</span>
        </template>
        <el-menu-item 
          v-for="child in item.children" 
          :key="child.index" 
          :index="child.index"
          @click="handleClick(child)"
          :class="{ 'active-menu-item': child.path === activePath }"
        >
          {{ child.title }}
        </el-menu-item>
      </el-sub-menu>
    </template>
  </el-menu>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  menuData: {
    type: Array,
    required: true
  },
  activePath: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['menu-click'])

const activeMenuItem = computed(() => {
  // Find the corresponding menu item index based on the current path
  for (const item of props.menuData) {
    const child = item.children?.find(child => child.path === props.activePath)
    if (child) {
      return child.index
    }
  }
  return ''
})

const handleClick = (item) => {
  emit('menu-click', item)
}
</script>

<style scoped>
.side-menu {
  height: 100%;
  border-right: none;
}

.active-menu-item {
  color: #1890ff !important;
}

:deep(.el-menu-item.is-active) {
  color: #1890ff !important;
  background-color: #e6f7ff !important;
}

:deep(.el-sub-menu__title:hover),
:deep(.el-menu-item:hover) {
  background-color: rgba(0, 0, 0, 0.02) !important;
}

:deep(.el-menu-item) {
  margin: 4px 0;
}

:deep(.el-menu-item.is-active::after) {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #1890ff;
}
</style> 