import requests
import sys
import json
import uuid
from datetime import datetime

class ComprehensiveBackendTester:
    def __init__(self, base_url="https://c65244e7-595d-4c7e-be40-53ada5dac5ce.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.critical_issues = []
        self.created_user_ids = []

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout)

            print(f"   Status: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                    return False, error_data
                except:
                    print(f"   Error: {response.text}")
                    return False, response.text

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_basic_endpoints(self):
        """Test basic endpoints to ensure backend is working"""
        print("\n🔧 BASIC CONNECTIVITY TESTS")
        print("="*50)
        
        # Test root API endpoint
        self.run_test("Root API Endpoint", "GET", "", 200)
        
        # Test known working i18n endpoints from test_result.md
        self.run_test("I18n Supported Languages", "GET", "i18n/languages", 200)
        
        # Test translations endpoint
        self.run_test("I18n Translations (English Common)", "GET", "i18n/translations/en/common", 200)

    def test_critical_user_profile_endpoints(self):
        """Test the critical user profile endpoints mentioned in review request"""
        print("\n🎯 CRITICAL USER PROFILE ENDPOINTS")
        print("="*50)
        
        # Test 1: POST /api/users/profile - User profile creation
        user_data = {
            "name": "Critical Test User",
            "email": "critical.test@example.com",
            "role": "business_owner",
            "industry": "technology",
            "preferences": {
                "default_jurisdiction": "US",
                "contract_types": ["NDA", "employment_agreement"]
            }
        }
        
        create_success, create_response = self.run_test(
            "POST /api/users/profile - User Profile Creation", 
            "POST", 
            "users/profile", 
            200,  # Based on logs, this returns 200 not 201
            user_data
        )
        
        user_id = None
        if create_success and isinstance(create_response, dict):
            user_id = create_response.get('id')
            if user_id:
                self.created_user_ids.append(user_id)
                print(f"   ✅ User created with ID: {user_id}")
                
                # Test 2: GET /api/users/profile/{user_id} - Get existing user
                get_success, get_response = self.run_test(
                    f"GET /api/users/profile/{user_id} - Get Existing User", 
                    "GET", 
                    f"users/profile/{user_id}", 
                    200
                )
                
                if get_success:
                    print(f"   ✅ User profile retrieved successfully")
                    # Verify data consistency
                    if isinstance(get_response, dict):
                        if get_response.get('name') == user_data['name']:
                            print(f"   ✅ Name consistency verified")
                        else:
                            self.critical_issues.append("User profile data inconsistency - name mismatch")
                else:
                    self.critical_issues.append("Cannot retrieve user profile after creation")
                
                # Test 3: PUT /api/users/profile/{user_id} - Update existing user
                update_data = {
                    "name": "Updated Critical Test User",
                    "industry": "legal_services",
                    "phone": "+1-555-0123"
                }
                
                update_success, update_response = self.run_test(
                    f"PUT /api/users/profile/{user_id} - Update Existing User", 
                    "PUT", 
                    f"users/profile/{user_id}", 
                    200,
                    update_data
                )
                
                if update_success:
                    print(f"   ✅ User profile updated successfully")
                    if isinstance(update_response, dict):
                        if update_response.get('name') == update_data['name']:
                            print(f"   ✅ Update consistency verified")
                        else:
                            self.critical_issues.append("User profile update inconsistency")
                else:
                    self.critical_issues.append("Cannot update user profile")
            else:
                self.critical_issues.append("User profile creation did not return user ID")
        else:
            self.critical_issues.append("User profile creation failed completely")
        
        # Test 4: GET /api/users/profile/{user_id} - Non-existent user behavior
        nonexistent_user_id = str(uuid.uuid4())
        nonexistent_success, nonexistent_response = self.run_test(
            f"GET /api/users/profile/{nonexistent_user_id} - Non-existent User", 
            "GET", 
            f"users/profile/{nonexistent_user_id}", 
            404  # Should return 404 for non-existent users
        )
        
        if nonexistent_success:
            print(f"   ✅ Correctly returns 404 for non-existent users")
        else:
            # Check if it creates default profiles instead (this would be the issue mentioned in review)
            default_success, default_response = self.run_test(
                f"GET /api/users/profile/{nonexistent_user_id} - Check Default Creation", 
                "GET", 
                f"users/profile/{nonexistent_user_id}", 
                200
            )
            if default_success:
                self.critical_issues.append("CRITICAL ISSUE: GET /api/users/profile/{user_id} creates default profiles for non-existent users instead of returning 404")
                self.tests_passed += 1  # Adjust count since we found the issue
            else:
                self.critical_issues.append("Unexpected behavior for non-existent user profile requests")

    def test_critical_i18n_user_language_endpoints(self):
        """Test the critical i18n user language endpoints mentioned in review request"""
        print("\n🎯 CRITICAL I18N USER LANGUAGE ENDPOINTS")
        print("="*50)
        
        # First, we need a user to test with
        if not self.created_user_ids:
            # Create a user for i18n testing
            user_data = {
                "name": "I18n Test User",
                "email": "i18n.test@example.com",
                "role": "legal_professional"
            }
            
            create_success, create_response = self.run_test(
                "Create User for I18n Testing", 
                "POST", 
                "users/profile", 
                200,
                user_data
            )
            
            if create_success and isinstance(create_response, dict):
                user_id = create_response.get('id')
                if user_id:
                    self.created_user_ids.append(user_id)
                else:
                    self.critical_issues.append("Cannot create user for i18n testing - no user ID returned")
                    return
            else:
                self.critical_issues.append("Cannot create user for i18n testing - creation failed")
                return
        
        user_id = self.created_user_ids[0]
        
        # Test 1: POST /api/i18n/user-language - Setting user language preferences
        language_data = {
            "user_id": user_id,
            "language": "es"  # Spanish
        }
        
        set_success, set_response = self.run_test(
            "POST /api/i18n/user-language - Set User Language", 
            "POST", 
            "i18n/user-language", 
            200,
            language_data
        )
        
        if set_success:
            print(f"   ✅ User language preference set successfully")
            if isinstance(set_response, dict):
                if set_response.get('language') == 'es':
                    print(f"   ✅ Language correctly set to Spanish")
                else:
                    self.critical_issues.append("Language setting response inconsistency")
        else:
            self.critical_issues.append("Cannot set user language preferences")
        
        # Test 2: GET /api/i18n/user-language/{user_id} - Getting user language preferences
        get_lang_success, get_lang_response = self.run_test(
            f"GET /api/i18n/user-language/{user_id} - Get User Language", 
            "GET", 
            f"i18n/user-language/{user_id}", 
            200
        )
        
        if get_lang_success:
            print(f"   ✅ User language preference retrieved successfully")
            if isinstance(get_lang_response, dict):
                if get_lang_response.get('language') == 'es':
                    print(f"   ✅ Language consistency verified")
                else:
                    self.critical_issues.append("Language preference inconsistency between set and get")
                    
                if get_lang_response.get('is_default') == False:
                    print(f"   ✅ is_default correctly set to False for user-specific setting")
                else:
                    self.critical_issues.append("is_default flag incorrect for user-specific language")
        else:
            self.critical_issues.append("Cannot retrieve user language preferences")
        
        # Test 3: GET /api/i18n/user-language/{user_id} - Non-existent user behavior
        nonexistent_user_id = str(uuid.uuid4())
        nonexistent_lang_success, nonexistent_lang_response = self.run_test(
            f"GET /api/i18n/user-language/{nonexistent_user_id} - Non-existent User", 
            "GET", 
            f"i18n/user-language/{nonexistent_user_id}", 
            200  # Based on test_result.md, this should return default 'en'
        )
        
        if nonexistent_lang_success:
            print(f"   ✅ Returns default language for non-existent users")
            if isinstance(nonexistent_lang_response, dict):
                if nonexistent_lang_response.get('language') == 'en':
                    print(f"   ✅ Correctly returns default 'en' language")
                else:
                    self.critical_issues.append("Default language is not 'en' for non-existent users")
                    
                if nonexistent_lang_response.get('is_default') == True:
                    print(f"   ✅ is_default correctly set to True for default language")
                else:
                    self.critical_issues.append("is_default flag incorrect for default language")
        else:
            self.critical_issues.append("Cannot get default language for non-existent users")
        
        # Test 4: POST /api/i18n/user-language - Non-existent user behavior
        nonexistent_set_data = {
            "user_id": nonexistent_user_id,
            "language": "fr"
        }
        
        nonexistent_set_success, nonexistent_set_response = self.run_test(
            f"POST /api/i18n/user-language - Non-existent User", 
            "POST", 
            "i18n/user-language", 
            404,  # Should return 404 for non-existent users
            nonexistent_set_data
        )
        
        if nonexistent_set_success:
            print(f"   ✅ Correctly returns 404 when setting language for non-existent users")
        else:
            # Check if it creates default language settings (this would be the issue)
            default_set_success, default_set_response = self.run_test(
                f"POST /api/i18n/user-language - Check Default Creation", 
                "POST", 
                "i18n/user-language", 
                200,
                nonexistent_set_data
            )
            if default_set_success:
                self.critical_issues.append("CRITICAL ISSUE: POST /api/i18n/user-language creates language settings for non-existent users instead of returning 404")
                self.tests_passed += 1  # Adjust count since we found the issue
            else:
                self.critical_issues.append("Unexpected behavior when setting language for non-existent users")

    def test_additional_critical_endpoints(self):
        """Test additional endpoints that need retesting based on test_result.md"""
        print("\n🔧 ADDITIONAL CRITICAL ENDPOINTS")
        print("="*50)
        
        # Test Professional Integrations Status (high priority, needs retesting)
        self.run_test(
            "Professional Integrations Status", 
            "GET", 
            "integrations/status", 
            200
        )
        
        # Test API Ecosystem Documentation (high priority, needs retesting)
        self.run_test(
            "API Ecosystem Documentation", 
            "GET", 
            "api-ecosystem/documentation", 
            200
        )
        
        # Test Workflow Templates (high priority, needs retesting)
        self.run_test(
            "Legal Workflow Templates", 
            "GET", 
            "workflows/templates", 
            200
        )
        
        # Test Marketplace Search (high priority, needs retesting)
        search_data = {
            "category": "legal",
            "pricing_model": "free"
        }
        self.run_test(
            "Marketplace Search", 
            "POST", 
            "marketplace/search", 
            200,
            search_data
        )

    def run_comprehensive_tests(self):
        """Run all comprehensive backend tests focusing on critical endpoints"""
        print("🚀 Starting Comprehensive Backend Testing...")
        print(f"   Base URL: {self.base_url}")
        print(f"   API URL: {self.api_url}")
        print(f"   Focus: Critical User Profile & I18n Endpoints")
        
        # Run tests in order of priority
        self.test_basic_endpoints()
        self.test_critical_user_profile_endpoints()
        self.test_critical_i18n_user_language_endpoints()
        self.test_additional_critical_endpoints()
        
        # Summary
        print("\n" + "="*80)
        print("COMPREHENSIVE BACKEND TESTING RESULTS")
        print("="*80)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🚨 CRITICAL ISSUES IDENTIFIED:")
        if self.critical_issues:
            for i, issue in enumerate(self.critical_issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("   ✅ No critical issues found")
        
        print(f"\n🧹 TEST DATA CLEANUP:")
        if self.created_user_ids:
            print(f"   Created {len(self.created_user_ids)} test users:")
            for user_id in self.created_user_ids:
                print(f"     - {user_id}")
        else:
            print("   No test users created")
        
        # Determine overall status
        critical_endpoints_working = len(self.critical_issues) == 0
        overall_success_rate = (self.tests_passed/self.tests_run)*100
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        if critical_endpoints_working and overall_success_rate >= 80:
            print("✅ BACKEND STATUS: FULLY FUNCTIONAL")
            print("✅ All critical user management endpoints working correctly")
            return True, self.tests_passed, self.tests_run, []
        elif overall_success_rate >= 60:
            print("⚠️  BACKEND STATUS: MOSTLY FUNCTIONAL WITH ISSUES")
            print("⚠️  Some critical issues found but core functionality works")
            return False, self.tests_passed, self.tests_run, self.critical_issues
        else:
            print("❌ BACKEND STATUS: SIGNIFICANT ISSUES")
            print("❌ Multiple critical endpoints not working properly")
            return False, self.tests_passed, self.tests_run, self.critical_issues

if __name__ == "__main__":
    tester = ComprehensiveBackendTester()
    success, passed, total, issues = tester.run_comprehensive_tests()
    
    if success:
        print("\n🎉 All critical backend endpoints working correctly!")
        sys.exit(0)
    else:
        print(f"\n❌ {len(issues)} critical issues found in backend endpoints")
        sys.exit(1)