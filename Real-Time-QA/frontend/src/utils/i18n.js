import { createI18n } from 'vue-i18n'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import enUs from 'element-plus/dist/locale/en.mjs'
import zhLocale from '@/locales/zh-CN'
import enLocale from '@/locales/en-US'
import { ref } from 'vue'

export const elementLocales = {
    'zh-CN': zhCn,
    'en-US': enUs
}

const messages = {
    'zh-CN': {
        ...zhLocale,
        ...zhCn
    },
    'en-US': {
        ...enLocale,
        ...enUs
    }
}

// Get browser language settings
export function getBrowserLanguage() {
    const language = navigator.language || navigator.userLanguage
    return language.startsWith('zh') ? 'zh-CN' : 'en-US'
}

// Create a reactive current language, default to English
export const currentLanguage = ref('en-US')

// Create i18n instance
const i18n = createI18n({
    legacy: false, // Use composition API
    locale: 'en-US', // Default language set to English
    fallbackLocale: 'en-US', // Set fallback language to English
    messages,
    globalInjection: true, // Global injection $t method
    silentTranslationWarn: true, // Disable translation warnings
    missingWarn: false // Disable missing translation warnings
})

// Switch language method
export async function setLanguage(lang) {
    console.log('setLanguage called, switching to:', lang)
    
    // If language is the same, do not switch
    if (currentLanguage.value === lang) {
        return Promise.resolve(lang)
    }
    
    try {
        const oldLang = currentLanguage.value
        
        // Update reactive reference
        currentLanguage.value = lang
        
        // Set i18n's locale
        i18n.global.locale.value = lang
        
        // Save to localStorage
        localStorage.setItem('language', lang)
        
        // Set HTML lang attribute
        document.documentElement.lang = lang
        
        // Trigger language change event
        window.dispatchEvent(new CustomEvent('languageChanged', { 
            detail: { 
                newLang: lang,
                oldLang: oldLang,
                timestamp: Date.now()
            }
        }))
        
        console.log('Language switch completed, current language:', currentLanguage.value)
        return Promise.resolve(lang)
    } catch (error) {
        console.error('Language switch failed:', error)
        return Promise.reject(error)
    }
}

// Export i18n instance
export default i18n 