import requests
import json
import uuid
from datetime import datetime

def test_professional_integrations_endpoints():
    """Test Professional Integrations Framework endpoints"""
    base_url = "https://c65244e7-595d-4c7e-be40-53ada5dac5ce.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🔧 PROFESSIONAL INTEGRATIONS FRAMEWORK TESTS")
    print("="*60)
    
    tests_run = 0
    tests_passed = 0
    
    # Test 1: Integration Status Endpoint
    tests_run += 1
    print(f"\n1. Testing Integration Status: {api_url}/integrations/status")
    try:
        response = requests.get(f"{api_url}/integrations/status", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Integration Status working")
            try:
                data = response.json()
                if 'integrations' in data:
                    integrations = data['integrations']
                    print(f"   Found {len(integrations)} integrations")
                    # Show first few integrations
                    for i, integration in enumerate(integrations[:3]):
                        print(f"     - {integration.get('name', 'Unknown')} ({integration.get('status', 'Unknown')})")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Integration Status failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Integration Activation Endpoint
    tests_run += 1
    print(f"\n2. Testing Integration Activation: {api_url}/integrations/activate")
    try:
        activation_data = {
            "integration_name": "google_drive",
            "configuration": {
                "api_key": "test_key",
                "enabled": True
            }
        }
        response = requests.post(f"{api_url}/integrations/activate", json=activation_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Integration Activation working")
            try:
                data = response.json()
                print(f"   Activation result: {data.get('status', 'Unknown')}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Integration Activation failed")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Error: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Integration Action Endpoint
    tests_run += 1
    print(f"\n3. Testing Integration Action: {api_url}/integrations/action")
    try:
        action_data = {
            "integration_name": "google_drive",
            "action": "list_documents",
            "parameters": {
                "folder_id": "root",
                "limit": 10
            }
        }
        response = requests.post(f"{api_url}/integrations/action", json=action_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Integration Action working")
            try:
                data = response.json()
                print(f"   Action result: {data.get('status', 'Unknown')}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Integration Action failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return tests_passed, tests_run

def test_professional_api_ecosystem_endpoints():
    """Test Professional API Ecosystem endpoints"""
    base_url = "https://c65244e7-595d-4c7e-be40-53ada5dac5ce.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("\n🔧 PROFESSIONAL API ECOSYSTEM TESTS")
    print("="*60)
    
    tests_run = 0
    tests_passed = 0
    
    # Test 1: API Key Generation
    tests_run += 1
    print(f"\n1. Testing API Key Generation: {api_url}/api-ecosystem/generate-key")
    try:
        key_data = {
            "organization_name": "Test Organization",
            "access_level": "professional",
            "rate_limit": 1000,
            "expires_in_days": 365
        }
        response = requests.post(f"{api_url}/api-ecosystem/generate-key", json=key_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ API Key Generation working")
            try:
                data = response.json()
                if 'api_key' in data:
                    print(f"   Generated API key: {data['api_key'][:20]}...")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ API Key Generation failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: API Documentation
    tests_run += 1
    print(f"\n2. Testing API Documentation: {api_url}/api-ecosystem/documentation")
    try:
        response = requests.get(f"{api_url}/api-ecosystem/documentation", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ API Documentation working")
            try:
                data = response.json()
                if 'endpoints' in data:
                    endpoints = data['endpoints']
                    print(f"   Found {len(endpoints)} documented endpoints")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ API Documentation failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Usage Analytics
    tests_run += 1
    print(f"\n3. Testing Usage Analytics: {api_url}/api-ecosystem/usage-analytics")
    try:
        response = requests.get(f"{api_url}/api-ecosystem/usage-analytics", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Usage Analytics working")
            try:
                data = response.json()
                print(f"   Analytics data structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Usage Analytics failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return tests_passed, tests_run

def test_legal_workflow_automation_endpoints():
    """Test Legal Workflow Automation endpoints"""
    base_url = "https://c65244e7-595d-4c7e-be40-53ada5dac5ce.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("\n🔧 LEGAL WORKFLOW AUTOMATION TESTS")
    print("="*60)
    
    tests_run = 0
    tests_passed = 0
    
    # Test 1: Workflow Templates
    tests_run += 1
    print(f"\n1. Testing Workflow Templates: {api_url}/workflows/templates")
    try:
        response = requests.get(f"{api_url}/workflows/templates", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Workflow Templates working")
            try:
                data = response.json()
                if 'templates' in data:
                    templates = data['templates']
                    print(f"   Found {len(templates)} workflow templates")
                    for template in templates[:3]:
                        print(f"     - {template.get('name', 'Unknown')} ({template.get('category', 'Unknown')})")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Workflow Templates failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Workflow Creation
    tests_run += 1
    print(f"\n2. Testing Workflow Creation: {api_url}/workflows/create")
    try:
        workflow_data = {
            "template_name": "client_onboarding",
            "client_name": "Test Client",
            "parameters": {
                "client_type": "individual",
                "services": ["contract_review", "legal_consultation"]
            }
        }
        response = requests.post(f"{api_url}/workflows/create", json=workflow_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Workflow Creation working")
            try:
                data = response.json()
                workflow_id = data.get('workflow_id')
                if workflow_id:
                    print(f"   Created workflow ID: {workflow_id}")
                    
                    # Test 3: Workflow Status
                    tests_run += 1
                    print(f"\n3. Testing Workflow Status: {api_url}/workflows/{workflow_id}/status")
                    try:
                        response = requests.get(f"{api_url}/workflows/{workflow_id}/status", timeout=10)
                        print(f"   Status: {response.status_code}")
                        if response.status_code == 200:
                            tests_passed += 1
                            print(f"   ✅ Workflow Status working")
                            try:
                                data = response.json()
                                print(f"   Workflow status: {data.get('status', 'Unknown')}")
                                print(f"   Progress: {data.get('progress_percentage', 0)}%")
                            except:
                                print(f"   Response: {response.text[:200]}...")
                        else:
                            print(f"   ❌ Workflow Status failed")
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Workflow Creation failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Workflow Analytics
    tests_run += 1
    print(f"\n4. Testing Workflow Analytics: {api_url}/workflows/analytics")
    try:
        response = requests.get(f"{api_url}/workflows/analytics", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Workflow Analytics working")
            try:
                data = response.json()
                print(f"   Analytics structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Workflow Analytics failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return tests_passed, tests_run

def test_marketplace_partnership_endpoints():
    """Test Marketplace & Partnership Ecosystem endpoints"""
    base_url = "https://c65244e7-595d-4c7e-be40-53ada5dac5ce.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("\n🔧 MARKETPLACE & PARTNERSHIP ECOSYSTEM TESTS")
    print("="*60)
    
    tests_run = 0
    tests_passed = 0
    
    # Test 1: Marketplace Search
    tests_run += 1
    print(f"\n1. Testing Marketplace Search: {api_url}/marketplace/search")
    try:
        search_data = {
            "category": "legal",
            "pricing_model": "free",
            "rating_min": 4.0
        }
        response = requests.post(f"{api_url}/marketplace/search", json=search_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Marketplace Search working")
            try:
                data = response.json()
                if 'apps' in data:
                    apps = data['apps']
                    print(f"   Found {len(apps)} apps")
                    for app in apps[:3]:
                        print(f"     - {app.get('name', 'Unknown')} (Rating: {app.get('rating', 'N/A')})")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Marketplace Search failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Partnership Application
    tests_run += 1
    print(f"\n2. Testing Partnership Application: {api_url}/partnerships/apply")
    try:
        partnership_data = {
            "organization_name": "Test Legal Tech Company",
            "partner_type": "technology_partner",
            "business_info": {
                "website": "https://testlegaltech.com",
                "description": "AI-powered legal document analysis",
                "employees": "10-50"
            },
            "contact_info": {
                "name": "John Doe",
                "email": "john@testlegaltech.com",
                "phone": "+1-555-0123"
            }
        }
        response = requests.post(f"{api_url}/partnerships/apply", json=partnership_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Partnership Application working")
            try:
                data = response.json()
                print(f"   Application status: {data.get('status', 'Unknown')}")
                print(f"   Application ID: {data.get('application_id', 'Unknown')}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Partnership Application failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Partner Search
    tests_run += 1
    print(f"\n3. Testing Partner Search: {api_url}/partnerships/search")
    try:
        response = requests.get(f"{api_url}/partnerships/search?partner_type=technology_partner", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tests_passed += 1
            print(f"   ✅ Partner Search working")
            try:
                data = response.json()
                if 'partners' in data:
                    partners = data['partners']
                    print(f"   Found {len(partners)} partners")
                    for partner in partners[:3]:
                        print(f"     - {partner.get('name', 'Unknown')} ({partner.get('type', 'Unknown')})")
                else:
                    print(f"   Response structure: {list(data.keys())}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Partner Search failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return tests_passed, tests_run

def run_comprehensive_backend_tests():
    """Run comprehensive backend tests for all high-priority endpoints"""
    print("🚀 COMPREHENSIVE BACKEND API TESTING")
    print("="*80)
    print("Testing all high-priority endpoints that need retesting...")
    
    total_tests = 0
    total_passed = 0
    
    # Test Professional Integrations Framework
    passed, run = test_professional_integrations_endpoints()
    total_passed += passed
    total_tests += run
    
    # Test Professional API Ecosystem
    passed, run = test_professional_api_ecosystem_endpoints()
    total_passed += passed
    total_tests += run
    
    # Test Legal Workflow Automation
    passed, run = test_legal_workflow_automation_endpoints()
    total_passed += passed
    total_tests += run
    
    # Test Marketplace & Partnership Ecosystem
    passed, run = test_marketplace_partnership_endpoints()
    total_passed += passed
    total_tests += run
    
    # Summary
    print("\n" + "="*80)
    print("COMPREHENSIVE BACKEND TESTING SUMMARY")
    print("="*80)
    print(f"Total Tests Run: {total_tests}")
    print(f"Tests Passed: {total_passed}")
    print(f"Tests Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 ALL BACKEND ENDPOINTS WORKING PERFECTLY!")
        return True
    elif (total_passed/total_tests) >= 0.8:
        print(f"\n✅ BACKEND MOSTLY FUNCTIONAL ({(total_passed/total_tests)*100:.1f}% success rate)")
        return True
    else:
        print(f"\n⚠️  BACKEND HAS SOME ISSUES ({(total_passed/total_tests)*100:.1f}% success rate)")
        return False

if __name__ == "__main__":
    success = run_comprehensive_backend_tests()
    if success:
        print("\n✅ Backend testing completed successfully!")
    else:
        print("\n❌ Backend testing found some issues")