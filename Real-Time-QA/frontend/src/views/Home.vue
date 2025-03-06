<template>
  <el-container class="layout-container">
    <el-header class="headerView" height="9rem">
      <div class="header-title">
        <span class="title-text">Agentographer</span>
        <span class="title-subtitle">{{ currentTitle }}</span>
      </div>
      <el-button 
        class="lang-switch" 
        type="primary" 
        text
        @click="toggleLanguage"
      >
        {{ currentLang === 'en-US' ? 'Chinese' : 'English' }}
      </el-button>
    </el-header>
    <el-container class="main-container">
      <el-aside width="21rem">
        <side-menu
          :menu-data="menuData"
          :active-path="currentPath"
          @menu-click="handleMenuClick"
        />
      </el-aside>
      <el-main class="content-main">
        <transition name="fade-transform" mode="out-in">
          <div class="chat-wrapper" v-if="currentPath === '/real-time-qa'" key="realtime">
            <RealTimeQA />
          </div>
          <!-- <div class="chat-wrapper" v-else-if="currentPath === '/isocenter'" key="realtimei">
            <RealTimeQAI />
          </div> -->
          <div v-else class="welcome-content" key="welcome">
            <h2>{{ t('welcome.title') }}</h2>
            <p>{{ t('welcome.subtitle') }}</p>
          </div>
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'

import RealTimeQA from '@/views/RealTimeQA.vue'
import { Monitor, Camera, FirstAidKit } from '@element-plus/icons-vue'
import { elementLocales, setLanguage, currentLanguage } from '@/utils/i18n'

const { t, locale } = useI18n()
const currentLang = computed(() => currentLanguage.value)

//  i18n synchronizes locale and currentLanguage
watch(currentLanguage, (newLang) => {
  if (locale.value !== newLang) {
    locale.value = newLang
  }
}, { immediate: true })


const toggleLanguage = async () => {
  const newLang = currentLang.value === 'en-US' ? 'zh-CN' : 'en-US'

  
  try {
    await setLanguage(newLang)
  } catch (error) {
    console.error('Language switch failed:', error)
  }
}

const currentPath = ref('/llamma-ct')


watch(() => currentLanguage.value, () => {
  console.log('Language changes, update menu data')
})

const menuData = computed(() => {

  return [
    {
      index: '1',
      title: t('menu.Large Language Models'),
      icon: Monitor,
      children: [
        { index: '1-2', title: t('menu.Real-Time Q&A'), path: '/real-time-qa' }
      ]
    }
  ]
})


const currentTitle = computed(() => {
  for (const menu of menuData.value) {
    const matchedItem = menu.children.find(item => item.path === currentPath.value)
    if (matchedItem) {
      return `${t(menu.title)} - ${t(matchedItem.title)}`
    }
  }
  return t('common.systemTitle') 
})

const handleMenuClick = (item) => {

  currentPath.value = item.path
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}

.main-container {
  flex: 1;
  display: flex;
  background: rgb(244,245,246);
  background: linear-gradient(90deg, rgba(244,245,246,1) 5%, rgba(204,209,238,1) 58%);
}

.el-header {
  border-bottom: 1px solid #dcdfe6;
  color: #333;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(244,245,246);
  background: linear-gradient(90deg, rgba(244,245,246,1) 5%, rgba(204,209,238,1) 58%);
}

.header-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.title-text {
  font-size: 3.2rem;
  font-weight: 600;
  background: linear-gradient(120deg, #1a237e, #0d47a1);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: 2px;
}

.title-subtitle {
  font-size: 1.4rem;
  color: #666;
  font-weight: 400;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.el-aside {
  color: #333;
  border-right: 1px solid #dcdfe6;
  padding: 0;
  flex-shrink: 0;
}

.el-main {
  flex: 1;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.chat-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.welcome-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #666;
}

.welcome-content h2 {
  margin-bottom: 1rem;
  font-size: 2rem;
  font-weight: 500;
}

.welcome-content p {
  font-size: 1.2rem;
}

.el-menu {
  background: none;
}


.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 1s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-enter-to,
.fade-transform-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.headerView {
  position: relative;
  border-bottom: 1px solid #dcdfe6;
  color: #333;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgb(244,245,246);
  background: linear-gradient(90deg, rgba(244,245,246,1) 5%, rgba(204,209,238,1) 58%);
}

.lang-switch {
  position: absolute;
  right: 2rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  border-radius: 2rem;
  transition: all 0.3s ease;
  color: #409EFF;
}

.lang-switch:hover {
  background: rgba(64, 158, 255, 0.1);
  color: #66b1ff;
}

.lang-switch .el-icon {
  font-size: 1.2rem;
}
</style>