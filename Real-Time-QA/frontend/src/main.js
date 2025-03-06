import { createApp } from 'vue'
import './style.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import { createI18n } from 'vue-i18n'
import zhCN from './locales/zh-CN'
import enUS from './locales/en-US'

function setRem() {
    const baseFontSize = 10;
    const windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    const designWidth = windowWidth;
    const rem = (windowWidth / designWidth) * baseFontSize;
    document.documentElement.style.fontSize = rem + 'px';
}
setRem();

const app = createApp(App)
app.use(router)
app.use(ElementPlus)

const i18n = createI18n({
  legacy: false,
  locale: 'zh-CN',
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS
  }
})

app.use(i18n)
app.mount('#app')

