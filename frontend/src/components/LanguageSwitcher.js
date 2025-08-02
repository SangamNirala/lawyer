import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { LanguageUtils } from '../i18n';
import { Globe, ChevronDown, Check } from 'lucide-react';

const LanguageSwitcher = ({ userId = null, className = '', showLabel = true }) => {
  const { t, i18n } = useTranslation('common');
  const [isOpen, setIsOpen] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language);
  const [isChanging, setIsChanging] = useState(false);

  const supportedLanguages = LanguageUtils.getSupportedLanguages();

  useEffect(() => {
    setCurrentLanguage(i18n.language);
  }, [i18n.language]);

  const handleLanguageChange = async (languageCode) => {
    if (languageCode === currentLanguage || isChanging) return;

    setIsChanging(true);
    setIsOpen(false);

    try {
      const success = await LanguageUtils.changeLanguage(languageCode, userId);
      
      if (success) {
        setCurrentLanguage(languageCode);
        
        // Show success notification (optional)
        if (window.showNotification) {
          window.showNotification(
            t('language.change_success', { 
              language: LanguageUtils.getLanguageName(languageCode) 
            }) || `Language changed to ${LanguageUtils.getLanguageName(languageCode)}`,
            'success'
          );
        }
      } else {
        console.error('Failed to change language');
      }
    } catch (error) {
      console.error('Error changing language:', error);
    } finally {
      setIsChanging(false);
    }
  };

  const currentLangInfo = supportedLanguages.find(lang => lang.code === currentLanguage);

  return (
    <div className={`relative inline-block text-left ${className}`}>
      <button
        type="button"
        className="inline-flex items-center justify-center w-full px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        onClick={() => setIsOpen(!isOpen)}
        disabled={isChanging}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <Globe className="w-4 h-4 mr-2" />
        {showLabel && (
          <span className="mr-1">
            {currentLangInfo?.nativeName || 'English'}
          </span>
        )}
        {isChanging ? (
          <div className="w-4 h-4 ml-1 animate-spin">
            <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-600 rounded-full"></div>
          </div>
        ) : (
          <ChevronDown className="w-4 h-4 ml-1" />
        )}
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown menu */}
          <div className="absolute right-0 z-20 w-56 mt-2 origin-top-right bg-white border border-gray-200 divide-y divide-gray-100 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div className="px-4 py-3 bg-gray-50">
              <p className="text-sm font-medium text-gray-900">
                {t('language.select')}
              </p>
              <p className="text-sm text-gray-500">
                {t('language.current')}: {currentLangInfo?.nativeName}
              </p>
            </div>
            
            <div className="py-1" role="menu" aria-orientation="vertical">
              {supportedLanguages.map((language) => (
                <button
                  key={language.code}
                  onClick={() => handleLanguageChange(language.code)}
                  className="flex items-center justify-between w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50"
                  role="menuitem"
                  disabled={isChanging || language.code === currentLanguage}
                >
                  <div className="flex items-center">
                    <div className="flex flex-col">
                      <span className="font-medium">{language.nativeName}</span>
                      <span className="text-xs text-gray-500">{language.name}</span>
                    </div>
                  </div>
                  
                  {language.code === currentLanguage && (
                    <Check className="w-4 h-4 text-blue-600" />
                  )}
                </button>
              ))}
            </div>
            
            <div className="px-4 py-3 bg-gray-50">
              <p className="text-xs text-gray-500">
                {t('language.auto_detect')}: {t('language.browser_default')}
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default LanguageSwitcher;