import requests
import json
import uuid

def test_basic_connectivity():
    """Test basic connectivity to the API"""
    base_url = "https://c65244e7-595d-4c7e-be40-53ada5dac5ce.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🔍 Testing Basic API Connectivity...")
    
    try:
        # Test 1: Root API endpoint
        print(f"\n1. Testing Root API: {api_url}/")
        response = requests.get(f"{api_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Root API working")
            try:
                data = response.json()
                print(f"   Response: {data}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   ❌ Root API failed")
            return False
            
        # Test 2: Known working endpoint (i18n languages)
        print(f"\n2. Testing I18n Languages: {api_url}/i18n/languages")
        response = requests.get(f"{api_url}/i18n/languages", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ I18n Languages working")
            try:
                data = response.json()
                print(f"   Found {len(data.get('languages', []))} languages")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   ❌ I18n Languages failed")
            
        # Test 3: User profile creation (the critical endpoint)
        print(f"\n3. Testing User Profile Creation: {api_url}/users/profile")
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "role": "business_owner"
        }
        response = requests.post(f"{api_url}/users/profile", json=user_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ User Profile Creation working")
            try:
                data = response.json()
                user_id = data.get('id')
                print(f"   Created user ID: {user_id}")
                
                # Test 4: Get the created user profile
                if user_id:
                    print(f"\n4. Testing User Profile Retrieval: {api_url}/users/profile/{user_id}")
                    response = requests.get(f"{api_url}/users/profile/{user_id}", timeout=10)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        print(f"   ✅ User Profile Retrieval working")
                        try:
                            data = response.json()
                            print(f"   Retrieved user: {data.get('name')} ({data.get('email')})")
                        except:
                            print(f"   Response: {response.text}")
                    else:
                        print(f"   ❌ User Profile Retrieval failed")
                        
                    # Test 5: I18n user language setting
                    print(f"\n5. Testing I18n User Language Setting: {api_url}/i18n/user-language")
                    lang_data = {
                        "user_id": user_id,
                        "language": "es"
                    }
                    response = requests.post(f"{api_url}/i18n/user-language", json=lang_data, timeout=10)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        print(f"   ✅ I18n User Language Setting working")
                        try:
                            data = response.json()
                            print(f"   Set language: {data.get('language')} for user {data.get('user_id')}")
                        except:
                            print(f"   Response: {response.text}")
                            
                        # Test 6: I18n user language retrieval
                        print(f"\n6. Testing I18n User Language Retrieval: {api_url}/i18n/user-language/{user_id}")
                        response = requests.get(f"{api_url}/i18n/user-language/{user_id}", timeout=10)
                        print(f"   Status: {response.status_code}")
                        if response.status_code == 200:
                            print(f"   ✅ I18n User Language Retrieval working")
                            try:
                                data = response.json()
                                print(f"   Retrieved language: {data.get('language')} (is_default: {data.get('is_default')})")
                            except:
                                print(f"   Response: {response.text}")
                        else:
                            print(f"   ❌ I18n User Language Retrieval failed")
                    else:
                        print(f"   ❌ I18n User Language Setting failed")
                        try:
                            error_data = response.json()
                            print(f"   Error: {error_data}")
                        except:
                            print(f"   Error: {response.text}")
            except Exception as e:
                print(f"   Error parsing response: {e}")
                print(f"   Response: {response.text}")
        else:
            print(f"   ❌ User Profile Creation failed")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Error: {response.text}")
                
        # Test 7: Non-existent user behavior
        print(f"\n7. Testing Non-existent User Behavior")
        nonexistent_id = str(uuid.uuid4())
        
        # Test GET for non-existent user
        print(f"   7a. GET /api/users/profile/{nonexistent_id}")
        response = requests.get(f"{api_url}/users/profile/{nonexistent_id}", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly returns 404 for non-existent user")
        elif response.status_code == 200:
            print(f"   ⚠️  ISSUE: Returns 200 (creates default profile) instead of 404")
            try:
                data = response.json()
                print(f"   Default profile created: {data}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   ❌ Unexpected status for non-existent user")
            
        # Test I18n GET for non-existent user
        print(f"   7b. GET /api/i18n/user-language/{nonexistent_id}")
        response = requests.get(f"{api_url}/i18n/user-language/{nonexistent_id}", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Returns default language for non-existent user")
            try:
                data = response.json()
                print(f"   Default language: {data.get('language')} (is_default: {data.get('is_default')})")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   ❌ Unexpected behavior for non-existent user language")
            
        # Test I18n POST for non-existent user
        print(f"   7c. POST /api/i18n/user-language (non-existent user)")
        lang_data = {
            "user_id": nonexistent_id,
            "language": "fr"
        }
        response = requests.post(f"{api_url}/i18n/user-language", json=lang_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly returns 404 for non-existent user")
        elif response.status_code == 200:
            print(f"   ⚠️  ISSUE: Creates language setting for non-existent user")
            try:
                data = response.json()
                print(f"   Created setting: {data}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   ❌ Unexpected status for non-existent user language setting")
            
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Backend API Test")
    print("="*50)
    success = test_basic_connectivity()
    if success:
        print(f"\n✅ Basic connectivity test completed")
    else:
        print(f"\n❌ Basic connectivity test failed")