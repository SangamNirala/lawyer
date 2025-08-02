import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import enCommon from './locales/en/common.json';
import esCommon from './locales/es/common.json';
import frCommon from './locales/fr/common.json';
import deCommon from './locales/de/common.json';

// Translation resources
const resources = {
  en: {
    common: enCommon
  },
  es: {
    common: esCommon
  },
  fr: {
    common: frCommon
  },
  de: {
    common: deCommon
  }
};

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Custom backend for dynamic translations
const Backend = {
  type: 'backend',
  
  async read(language, namespace, callback) {
    try {
      // First try to get from local resources
      if (resources[language] && resources[language][namespace]) {
        callback(null, resources[language][namespace]);
        return;
      }
      
      // If not found locally, try to fetch from backend API
      const response = await fetch(`${BACKEND_URL}/api/i18n/translations/${language}/${namespace}`);
      
      if (response.ok) {
        const data = await response.json();
        callback(null, data.translations);
      } else {
        // Fallback to English if available
        if (language !== 'en' && resources.en && resources.en[namespace]) {
          callback(null, resources.en[namespace]);
        } else {
          callback(new Error(`Translation not found: ${language}/${namespace}`), false);
        }
      }
    } catch (error) {
      console.warn(`Failed to load translations for ${language}/${namespace}:`, error);
      
      // Fallback to English if available
      if (language !== 'en' && resources.en && resources.en[namespace]) {
        callback(null, resources.en[namespace]);
      } else {
        callback(error, false);
      }
    }
  }
};

// User preferences management
export const UserLanguagePreferences = {
  async getUserLanguage(userId) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/i18n/user-language/${userId}`);
      if (response.ok) {
        const data = await response.json();
        return data.language;
      }
    } catch (error) {
      console.warn('Failed to get user language preference:', error);
    }
    return null;
  },
  
  async setUserLanguage(userId, language) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/i18n/user-language`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          language: language
        })
      });
      
      if (response.ok) {
        return true;
      }
    } catch (error) {
      console.warn('Failed to set user language preference:', error);
    }
    return false;
  }
};

// Language detection configuration
const languageDetector = new LanguageDetector();
languageDetector.addDetector({
  name: 'userPreference',
  
  async: true,
  
  lookup: async function(options) {
    // Try to get user preference from localStorage first
    const storedUserId = localStorage.getItem('userId');
    const storedLanguage = localStorage.getItem('userLanguage');
    
    if (storedUserId && storedLanguage) {
      return storedLanguage;
    }
    
    // If user is logged in, try to get their preference from backend
    if (storedUserId) {
      try {
        const userLanguage = await UserLanguagePreferences.getUserLanguage(storedUserId);
        if (userLanguage) {
          localStorage.setItem('userLanguage', userLanguage);
          return userLanguage;
        }
      } catch (error) {
        console.warn('Failed to detect user language preference:', error);
      }
    }
    
    // Fallback to browser language detection
    const browserLang = navigator.language || navigator.userLanguage || 'en';
    const supportedLanguages = ['en', 'es', 'fr', 'de'];
    const detectedLang = browserLang.split('-')[0];
    
    return supportedLanguages.includes(detectedLang) ? detectedLang : 'en';
  }
});

// Initialize i18next
i18n
  .use(Backend)
  .use(languageDetector)
  .use(initReactI18next)
  .init({
    // Default language
    fallbackLng: 'en',
    
    // Supported languages
    supportedLngs: ['en', 'es', 'fr', 'de'],
    
    // Language detection options
    detection: {
      order: ['userPreference', 'localStorage', 'navigator', 'htmlTag'],
      lookupLocalStorage: 'userLanguage',
      caches: ['localStorage'],
      excludeCacheFor: ['cimode'],
      checkWhitelist: true
    },
    
    // Default namespace
    defaultNS: 'common',
    ns: ['common'],
    
    // Interpolation options
    interpolation: {
      escapeValue: false // React already does escaping
    },
    
    // Debug mode (disable in production)
    debug: process.env.NODE_ENV === 'development',
    
    // Resources (for offline support)
    resources,
    
    // Backend options
    backend: {
      loadPath: '/api/i18n/translations/{{lng}}/{{ns}}'
    },
    
    // React options
    react: {
      bindI18n: 'languageChanged loaded',
      useSuspense: false // Prevent suspense issues
    },
    
    // Load resources synchronously
    initImmediate: false,
    
    // Always load synchronously
    load: 'languageOnly'
  });

// Helper functions for language management
export const LanguageUtils = {
  getCurrentLanguage: () => i18n.language,
  
  changeLanguage: async (language, userId = null) => {
    try {
      await i18n.changeLanguage(language);
      localStorage.setItem('userLanguage', language);
      
      // Update user preference in backend if user is logged in
      if (userId) {
        await UserLanguagePreferences.setUserLanguage(userId, language);
      }
      
      // Update HTML lang attribute
      document.documentElement.lang = language;
      
      return true;
    } catch (error) {
      console.error('Failed to change language:', error);
      return false;
    }
  },
  
  getSupportedLanguages: () => [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'es', name: 'Spanish', nativeName: 'Español' },
    { code: 'fr', name: 'French', nativeName: 'Français' },
    { code: 'de', name: 'German', nativeName: 'Deutsch' }
  ],
  
  getLanguageName: (code) => {
    if (!code) return 'Unknown';
    const languages = LanguageUtils.getSupportedLanguages();
    const language = languages.find(lang => lang.code === code);
    return language ? language.nativeName : code;
  },
  
  isRtlLanguage: (language) => {
    // Add RTL languages here when supported (Arabic, Hebrew, etc.)
    const rtlLanguages = [];
    return rtlLanguages.includes(language);
  }
};

// Set initial HTML lang attribute
document.documentElement.lang = i18n.language || 'en';

// Listen for language changes to update HTML lang attribute
i18n.on('languageChanged', (language) => {
  document.documentElement.lang = language;
  
  // Update text direction for RTL languages
  document.documentElement.dir = LanguageUtils.isRtlLanguage(language) ? 'rtl' : 'ltr';
});

export default i18n;