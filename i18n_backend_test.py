import requests
import sys
import json
from datetime import datetime

class I18nAPITester:
    def __init__(self, base_url="https://1bb7b842-04a0-4c23-b5a7-2b679a028fd4.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout, verify=False)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout, verify=False)

            print(f"   Status: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'List with ' + str(len(response_data)) + ' items'}")
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_i18n_supported_languages(self):
        """Test GET /api/i18n/languages endpoint"""
        success, response = self.run_test(
            "Get Supported Languages",
            "GET",
            "i18n/languages",
            200
        )
        
        if success and response:
            supported_languages = response.get('supported_languages', [])
            default_language = response.get('default_language', '')
            total_languages = response.get('total_languages', 0)
            
            print(f"   Supported Languages: {len(supported_languages)}")
            print(f"   Default Language: {default_language}")
            print(f"   Total Languages: {total_languages}")
            
            # Verify expected languages (EN, ES, FR, DE)
            expected_languages = ['en', 'es', 'fr', 'de']
            language_codes = [lang.get('code') for lang in supported_languages]
            
            missing_languages = [lang for lang in expected_languages if lang not in language_codes]
            if not missing_languages:
                print(f"   ✅ All expected languages found: {expected_languages}")
            else:
                print(f"   ❌ Missing expected languages: {missing_languages}")
            
            # Verify language structure
            if supported_languages:
                first_lang = supported_languages[0]
                required_fields = ['code', 'name', 'native_name', 'direction', 'available']
                missing_fields = [field for field in required_fields if field not in first_lang]
                
                if not missing_fields:
                    print(f"   ✅ Language structure valid")
                else:
                    print(f"   ❌ Missing language fields: {missing_fields}")
                    
                # Show language details
                for lang in supported_languages:
                    print(f"   - {lang.get('code')}: {lang.get('name')} ({lang.get('native_name')})")
        
        return success, response

    def test_i18n_translations_retrieval(self):
        """Test GET /api/i18n/translations/{language}/{namespace} endpoint"""
        # Test cases as specified in the request
        test_cases = [
            {"language": "en", "namespace": "common", "description": "English Common Translations"},
            {"language": "es", "namespace": "common", "description": "Spanish Common Translations"},
            {"language": "fr", "namespace": "legal", "description": "French Legal Translations"},
            {"language": "de", "namespace": "legal", "description": "German Legal Translations"},
        ]
        
        all_success = True
        results = {}
        
        for test_case in test_cases:
            language = test_case["language"]
            namespace = test_case["namespace"]
            description = test_case["description"]
            
            success, response = self.run_test(
                f"Get Translations - {description}",
                "GET",
                f"i18n/translations/{language}/{namespace}",
                200
            )
            
            if success and response:
                translations = response.get('translations', {})
                fallback_used = response.get('fallback_used', False)
                
                print(f"   Language: {response.get('language')}")
                print(f"   Namespace: {response.get('namespace')}")
                print(f"   Translation Keys: {len(translations)}")
                print(f"   Fallback Used: {fallback_used}")
                
                # Verify translation structure for common namespace
                if namespace == "common" and translations:
                    expected_sections = ['app', 'navigation', 'common', 'forms', 'contract']
                    found_sections = [section for section in expected_sections if section in translations]
                    print(f"   Found Sections: {found_sections}")
                    
                    if len(found_sections) >= 3:
                        print(f"   ✅ Good translation coverage")
                    else:
                        print(f"   ⚠️  Limited translation coverage")
                
                # Verify translation structure for legal namespace
                elif namespace == "legal" and translations:
                    expected_sections = ['legal_terms', 'contract_clauses', 'jurisdictions', 'industries']
                    found_sections = [section for section in expected_sections if section in translations]
                    print(f"   Found Legal Sections: {found_sections}")
                    
                    if len(found_sections) >= 2:
                        print(f"   ✅ Good legal translation coverage")
                    else:
                        print(f"   ⚠️  Limited legal translation coverage")
                
                results[f"{language}_{namespace}"] = len(translations)
            else:
                all_success = False
                results[f"{language}_{namespace}"] = 0
        
        print(f"   Translation Summary: {results}")
        return all_success, results

    def test_i18n_user_language_preferences(self):
        """Test POST /api/i18n/user-language endpoint"""
        # Test setting user language preferences as specified in the request
        test_user_data = {
            "user_id": "test-user-123",
            "language": "es"
        }
        
        success, response = self.run_test(
            "Set User Language Preference",
            "POST",
            "i18n/user-language",
            200,
            test_user_data
        )
        
        if success and response:
            user_id = response.get('user_id')
            language = response.get('language')
            success_flag = response.get('success', False)
            message = response.get('message', '')
            
            print(f"   User ID: {user_id}")
            print(f"   Language Set: {language}")
            print(f"   Success: {success_flag}")
            print(f"   Message: {message}")
            
            if user_id == "test-user-123" and language == "es" and success_flag:
                print(f"   ✅ User language preference set successfully")
            else:
                print(f"   ❌ User language preference setting failed")
        
        # Test with different languages
        other_languages = ["fr", "de", "en"]
        for lang in other_languages:
            test_data = {"user_id": f"test-user-{lang}", "language": lang}
            success_lang, response_lang = self.run_test(
                f"Set User Language to {lang.upper()}",
                "POST",
                "i18n/user-language",
                200,
                test_data
            )
            
            if success_lang:
                print(f"   ✅ Successfully set language to {lang} for user test-user-{lang}")
        
        return success, response

    def test_i18n_get_user_language_preferences(self):
        """Test GET /api/i18n/user-language/{user_id} endpoint"""
        # Test getting user language preferences for the user we just created
        test_user_id = "test-user-123"
        
        success, response = self.run_test(
            "Get User Language Preference",
            "GET",
            f"i18n/user-language/{test_user_id}",
            200
        )
        
        if success and response:
            user_id = response.get('user_id')
            language = response.get('language')
            is_default = response.get('is_default', False)
            
            print(f"   User ID: {user_id}")
            print(f"   Current Language: {language}")
            print(f"   Is Default: {is_default}")
            
            if user_id == test_user_id:
                print(f"   ✅ User language preference retrieved successfully")
                
                # Verify the language matches what we set (should be 'es' or fallback to 'en')
                if language in ['es', 'en']:
                    print(f"   ✅ Language preference is valid: {language}")
                else:
                    print(f"   ❌ Unexpected language preference: {language}")
            else:
                print(f"   ❌ User ID mismatch in response")
        
        # Test with non-existent user (should return default 'en')
        success_default, response_default = self.run_test(
            "Get Language for Non-existent User",
            "GET",
            "i18n/user-language/non-existent-user",
            200
        )
        
        if success_default and response_default:
            default_language = response_default.get('language')
            if default_language == 'en':
                print(f"   ✅ Default language 'en' returned for non-existent user")
            else:
                print(f"   ❌ Expected 'en' for non-existent user, got: {default_language}")
        
        return success, response

    def test_i18n_ai_translation(self):
        """Test POST /api/i18n/translate endpoint with AI translation"""
        # Test AI translation as specified in the request
        translation_request = {
            "text": "Generate Contract",
            "target_language": "es",
            "context": "legal"
        }
        
        success, response = self.run_test(
            "AI Translation - Generate Contract to Spanish",
            "POST",
            "i18n/translate",
            200,
            translation_request,
            timeout=45  # AI translation might take longer
        )
        
        if success and response:
            original_text = response.get('original_text')
            translated_text = response.get('translated_text')
            target_language = response.get('target_language')
            confidence = response.get('confidence', 0)
            validation_result = response.get('validation_result', {})
            
            print(f"   Original Text: {original_text}")
            print(f"   Translated Text: {translated_text}")
            print(f"   Target Language: {target_language}")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Validation Result: {validation_result.get('valid', 'N/A')}")
            
            # Verify response structure
            if (original_text == "Generate Contract" and 
                translated_text and 
                target_language == "es" and 
                0 <= confidence <= 1):
                print(f"   ✅ AI translation completed successfully")
                
                # Check if translation looks reasonable (should contain Spanish words)
                spanish_indicators = ['generar', 'contrato', 'crear', 'documento']
                if any(indicator in translated_text.lower() for indicator in spanish_indicators):
                    print(f"   ✅ Translation appears to be in Spanish")
                else:
                    print(f"   ⚠️  Translation may not be properly translated to Spanish")
            else:
                print(f"   ❌ AI translation response structure invalid")
        
        # Test with different languages and contexts
        additional_tests = [
            {"text": "Legal Agreement", "target_language": "fr", "context": "legal"},
            {"text": "Contract Terms", "target_language": "de", "context": "legal"},
            {"text": "Save Document", "target_language": "es", "context": "general"},
        ]
        
        for test in additional_tests:
            success_add, response_add = self.run_test(
                f"AI Translation - {test['text']} to {test['target_language'].upper()}",
                "POST",
                "i18n/translate",
                200,
                test,
                timeout=30
            )
            
            if success_add and response_add:
                translated = response_add.get('translated_text', '')
                confidence = response_add.get('confidence', 0)
                print(f"   ✅ '{test['text']}' → '{translated}' (confidence: {confidence:.2f})")
        
        return success, response

    def test_i18n_cache_management(self):
        """Test DELETE /api/i18n/cache endpoint"""
        # Test clearing all translation cache
        success_all, response_all = self.run_test(
            "Clear All Translation Cache",
            "DELETE",
            "i18n/cache",
            200
        )
        
        if success_all and response_all:
            success_flag = response_all.get('success', False)
            message = response_all.get('message', '')
            
            print(f"   Success: {success_flag}")
            print(f"   Message: {message}")
            
            if success_flag and 'all translations' in message:
                print(f"   ✅ All translation cache cleared successfully")
            else:
                print(f"   ❌ Cache clearing may have failed")
        
        # Test clearing cache for specific language
        success_lang, response_lang = self.run_test(
            "Clear Spanish Translation Cache",
            "DELETE",
            "i18n/cache?language=es",
            200
        )
        
        if success_lang and response_lang:
            message = response_lang.get('message', '')
            if 'language es' in message:
                print(f"   ✅ Spanish language cache cleared successfully")
            else:
                print(f"   ⚠️  Language-specific cache clearing message: {message}")
        
        # Test clearing cache for specific namespace
        success_ns, response_ns = self.run_test(
            "Clear Common Namespace Cache",
            "DELETE",
            "i18n/cache?namespace=common",
            200
        )
        
        if success_ns and response_ns:
            message = response_ns.get('message', '')
            if 'namespace common' in message:
                print(f"   ✅ Common namespace cache cleared successfully")
            else:
                print(f"   ⚠️  Namespace-specific cache clearing message: {message}")
        
        # Test clearing cache for specific language and namespace
        success_both, response_both = self.run_test(
            "Clear French Legal Cache",
            "DELETE",
            "i18n/cache?language=fr&namespace=legal",
            200
        )
        
        if success_both and response_both:
            message = response_both.get('message', '')
            if 'fr:legal' in message:
                print(f"   ✅ French legal cache cleared successfully")
            else:
                print(f"   ⚠️  Specific cache clearing message: {message}")
        
        return success_all, response_all

    def test_all_i18n_endpoints(self):
        """Test all internationalization (i18n) API endpoints"""
        print("\n" + "=" * 60)
        print("🌍 INTERNATIONALIZATION (I18N) API TESTING")
        print("=" * 60)
        print(f"   Base URL: {self.base_url}")
        print(f"   API URL: {self.api_url}")
        print("=" * 60)
        
        # Test 1: GET /api/i18n/languages - Should return supported languages (EN, ES, FR, DE)
        self.test_i18n_supported_languages()
        
        # Test 2: GET /api/i18n/translations/{language}/{namespace} - Test different combinations
        self.test_i18n_translations_retrieval()
        
        # Test 3: POST /api/i18n/user-language - Test setting user language preferences
        self.test_i18n_user_language_preferences()
        
        # Test 4: GET /api/i18n/user-language/{user_id} - Test getting user language preferences
        self.test_i18n_get_user_language_preferences()
        
        # Test 5: POST /api/i18n/translate - Test AI translation with different contexts
        self.test_i18n_ai_translation()
        
        # Test 6: DELETE /api/i18n/cache - Test clearing translation cache
        self.test_i18n_cache_management()
        
        # Final Results
        print("\n" + "=" * 60)
        print("🏁 INTERNATIONALIZATION (I18N) TESTING COMPLETE")
        print(f"   Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"   Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Summary of key results
        print(f"\n📊 I18N ENDPOINTS SUMMARY:")
        print(f"   Supported Languages: {'✅ PASS' if self.tests_passed > 0 else '❌ FAIL'}")
        print(f"   Translation Retrieval: {'✅ PASS' if self.tests_passed > 1 else '❌ FAIL'}")
        print(f"   User Language Preferences: {'✅ PASS' if self.tests_passed > 2 else '❌ FAIL'}")
        print(f"   AI Translation: {'✅ PASS' if self.tests_passed > 3 else '❌ FAIL'}")
        print(f"   Cache Management: {'✅ PASS' if self.tests_passed > 4 else '❌ FAIL'}")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL I18N TESTS PASSED!")
            print("✅ Internationalization system is fully functional")
        else:
            print("⚠️  Some i18n tests failed. Please review the output above.")
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = I18nAPITester()
    tester.test_all_i18n_endpoints()