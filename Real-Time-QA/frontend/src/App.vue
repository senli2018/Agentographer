<template>
  <el-config-provider :locale="elementLocales[currentLang]">
    <div class="app-container">
      <router-view />
    </div>
  </el-config-provider>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { elementLocales, currentLanguage } from '@/utils/i18n'

const { locale } = useI18n()
const currentLang = computed(() => currentLanguage.value)

// Synchronize i18n's locale and currentLanguage
watch(currentLanguage, (newLang) => {
  if (locale.value !== newLang) {
    locale.value = newLang
    console.log('App.vue language has been updated to:', newLang)
  }
}, { immediate: true })

// Listen for language change events
window.addEventListener('languageChanged', (event) => {
  console.log('App.vue received language change event:', event.detail)
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

#app {
  height: 100%;
  width: 100%;
}

.Apps {
  height: 100%;
  width: 100%;
}
</style>

<style scoped>
.app-container {
  position: relative;
  min-height: 100vh;
}
</style>

<style>
@import './assets/reset.css';
</style>

