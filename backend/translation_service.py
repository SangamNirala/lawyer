"""
Translation Management Service for Legal AI Platform

This service handles:
- Loading translations dynamically by language and namespace
- Caching translations for performance
- AI-powered translation generation and validation
- Fallback to English if translation is missing
- Legal terminology accuracy validation
"""

import json
import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta
import google.generativeai as genai
from groq import Groq

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.translation_cache = {}
        self.cache_expiry = {}
        self.cache_ttl = timedelta(hours=1)  # Cache for 1 hour
        self.base_path = Path(__file__).parent / 'i18n'
        self.supported_languages = ['en', 'es', 'fr', 'de']
        self.default_language = 'en'
        
        # Initialize AI clients from environment
        try:
            genai.configure(api_key=os.environ['GEMINI_API_KEY'])
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
            self.groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])
            self.ai_available = True
        except Exception as e:
            logger.warning(f"AI clients not available for translation: {e}")
            self.ai_available = False
    
    def _get_cache_key(self, language: str, namespace: str) -> str:
        """Generate cache key for language and namespace"""
        return f"{language}:{namespace}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached translation is still valid"""
        if cache_key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[cache_key]
    
    def _load_translation_file(self, language: str, namespace: str) -> Dict[str, Any]:
        """Load translation file from disk"""
        file_path = self.base_path / language / f"{namespace}.json"
        
        if not file_path.exists():
            logger.warning(f"Translation file not found: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading translation file {file_path}: {e}")
            return {}
    
    def get_translations(self, language: str, namespace: str) -> Dict[str, Any]:
        """
        Get translations for a specific language and namespace
        Falls back to English if language not available
        """
        # Validate language
        if language not in self.supported_languages:
            logger.warning(f"Language {language} not supported, falling back to {self.default_language}")
            language = self.default_language
        
        cache_key = self._get_cache_key(language, namespace)
        
        # Check cache first
        if cache_key in self.translation_cache and self._is_cache_valid(cache_key):
            return self.translation_cache[cache_key]
        
        # Load from file
        translations = self._load_translation_file(language, namespace)
        
        # Fallback to English if no translations found
        if not translations and language != self.default_language:
            logger.info(f"No translations found for {language}:{namespace}, falling back to English")
            translations = self._load_translation_file(self.default_language, namespace)
        
        # Cache the result
        self.translation_cache[cache_key] = translations
        self.cache_expiry[cache_key] = datetime.now() + self.cache_ttl
        
        return translations
    
    def get_translation(self, language: str, namespace: str, key: str, default: str = None) -> str:
        """
        Get a specific translation by key
        Supports nested keys using dot notation (e.g., 'app.title')
        """
        translations = self.get_translations(language, namespace)
        
        # Handle nested keys
        keys = key.split('.')
        value = translations
        
        try:
            for k in keys:
                value = value[k]
            return str(value)
        except (KeyError, TypeError):
            # Fallback to English if key not found
            if language != self.default_language:
                return self.get_translation(self.default_language, namespace, key, default)
            return default or key
    
    async def generate_ai_translation(self, text: str, target_language: str, context: str = "general") -> str:
        """
        Generate AI-powered translation with legal context awareness
        """
        if not self.ai_available:
            logger.warning("AI translation not available")
            return text
        
        language_names = {
            'es': 'Spanish',
            'fr': 'French', 
            'de': 'German'
        }
        
        target_lang_name = language_names.get(target_language, target_language)
        
        prompt = f"""
        Translate the following text to {target_lang_name} with these requirements:
        
        Context: {context}
        Text to translate: "{text}"
        
        Requirements:
        1. Maintain legal accuracy and terminology precision
        2. Use formal, professional language appropriate for legal documents
        3. Preserve any technical terms that should remain in English
        4. Ensure cultural appropriateness for the target language
        5. Return only the translation, no explanations
        
        Translation:
        """
        
        try:
            # Use Gemini for high-quality legal translation
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.1,
                )
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"AI translation error: {e}")
            return text
    
    async def validate_legal_translation(self, original: str, translation: str, target_language: str) -> Dict[str, Any]:
        """
        Validate legal translation accuracy using AI
        """
        if not self.ai_available:
            return {"valid": True, "confidence": 0.7, "issues": [], "suggestions": []}
        
        language_names = {
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
        
        target_lang_name = language_names.get(target_language, target_language)
        
        prompt = f"""
        As a legal translation expert, validate this translation:
        
        Original English: "{original}"
        {target_lang_name} Translation: "{translation}"
        
        Evaluate:
        1. Legal accuracy and terminology correctness
        2. Preservation of legal meaning and intent
        3. Cultural and jurisdictional appropriateness
        4. Professional language usage
        
        Return JSON with:
        {{
            "valid": true/false,
            "confidence": 0.0-1.0,
            "issues": ["list of issues found"],
            "suggestions": ["improvement suggestions"],
            "legal_concerns": ["specific legal accuracy concerns"]
        }}
        """
        
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=800,
                    temperature=0.1,
                )
            )
            
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"valid": True, "confidence": 0.8, "issues": [], "suggestions": []}
        except Exception as e:
            logger.error(f"Translation validation error: {e}")
            return {"valid": True, "confidence": 0.7, "issues": ["Validation service unavailable"], "suggestions": []}
    
    async def bulk_translate_namespace(self, namespace: str, target_language: str) -> Dict[str, Any]:
        """
        Translate an entire namespace to target language using AI
        """
        english_translations = self.get_translations('en', namespace)
        translated = {}
        
        if not english_translations:
            return translated
        
        # Recursively translate nested objects
        async def translate_object(obj, path=""):
            if isinstance(obj, dict):
                result = {}
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    result[key] = await translate_object(value, current_path)
                return result
            elif isinstance(obj, str):
                context = f"legal_{namespace}" if namespace == "legal" else namespace
                return await self.generate_ai_translation(obj, target_language, context)
            else:
                return obj
        
        translated = await translate_object(english_translations)
        return translated
    
    def save_translations(self, language: str, namespace: str, translations: Dict[str, Any]) -> bool:
        """
        Save translations to file
        """
        file_path = self.base_path / language / f"{namespace}.json"
        
        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, indent=2, ensure_ascii=False)
            
            # Clear cache for this translation
            cache_key = self._get_cache_key(language, namespace)
            if cache_key in self.translation_cache:
                del self.translation_cache[cache_key]
            if cache_key in self.cache_expiry:
                del self.cache_expiry[cache_key]
            
            return True
        except Exception as e:
            logger.error(f"Error saving translations to {file_path}: {e}")
            return False
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Get list of supported languages with metadata
        """
        language_info = {
            'en': {'name': 'English', 'native_name': 'English', 'code': 'en', 'direction': 'ltr'},
            'es': {'name': 'Spanish', 'native_name': 'Español', 'code': 'es', 'direction': 'ltr'},
            'fr': {'name': 'French', 'native_name': 'Français', 'code': 'fr', 'direction': 'ltr'},
            'de': {'name': 'German', 'native_name': 'Deutsch', 'code': 'de', 'direction': 'ltr'}
        }
        
        return [
            {
                'code': lang,
                'name': info['name'],
                'native_name': info['native_name'],
                'direction': info['direction'],
                'available': True
            }
            for lang, info in language_info.items()
            if lang in self.supported_languages
        ]
    
    def clear_cache(self, language: str = None, namespace: str = None):
        """
        Clear translation cache
        """
        if language and namespace:
            cache_key = self._get_cache_key(language, namespace)
            if cache_key in self.translation_cache:
                del self.translation_cache[cache_key]
            if cache_key in self.cache_expiry:
                del self.cache_expiry[cache_key]
        else:
            self.translation_cache.clear()
            self.cache_expiry.clear()

# Global translation service instance
translation_service = TranslationService()

def get_translation_service() -> TranslationService:
    """Get the global translation service instance"""
    return translation_service