import requests
import sys
import json
import uuid
from datetime import datetime

class LegalQAAPITester:
    def __init__(self, base_url="https://585e8202-4886-4e9d-a484-d110c05ab5d6.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = str(uuid.uuid4())

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=120):
        """Run a single API test with extended timeout for RAG operations"""
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
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)

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

    def test_legal_qa_ask(self):
        """Test POST /api/legal-qa/ask - Legal question answering with RAG"""
        test_question = "What are the key elements required for a valid contract in the United States?"
        
        ask_data = {
            "question": test_question,
            "session_id": self.session_id,
            "context": {
                "jurisdiction": "US",
                "contract_type": "general"
            }
        }
        
        success, response = self.run_test(
            "Legal QA Ask - Contract Elements Question", 
            "POST", 
            "legal-qa/ask", 
            200, 
            ask_data,
            timeout=120  # Extended timeout for RAG processing
        )
        
        if success and isinstance(response, dict):
            print(f"   Question: {test_question}")
            
            # Check response structure
            expected_fields = ['answer', 'sources', 'confidence', 'session_id']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Response contains '{field}' field")
                else:
                    print(f"   ⚠️  Response missing '{field}' field")
            
            # Check answer quality
            answer = response.get('answer', '')
            if len(answer) > 50:
                print(f"   ✅ Answer has substantial content ({len(answer)} characters)")
            else:
                print(f"   ⚠️  Answer seems short ({len(answer)} characters)")
            
            # Check sources
            sources = response.get('sources', [])
            if sources and len(sources) > 0:
                print(f"   ✅ Found {len(sources)} sources")
                for i, source in enumerate(sources[:3]):  # Show first 3 sources
                    print(f"     - Source {i+1}: {source.get('title', 'No title')[:50]}...")
            else:
                print(f"   ⚠️  No sources found in response")
            
            # Check confidence score
            confidence = response.get('confidence', 0)
            if confidence > 0:
                print(f"   ✅ Confidence score: {confidence}")
            else:
                print(f"   ⚠️  No confidence score provided")
            
            # Check session ID
            returned_session_id = response.get('session_id')
            if returned_session_id == self.session_id:
                print(f"   ✅ Session ID correctly preserved")
            else:
                print(f"   ⚠️  Session ID mismatch: sent {self.session_id}, got {returned_session_id}")
                
        return success, response

    def test_legal_qa_stats(self):
        """Test GET /api/legal-qa/stats - RAG system statistics"""
        success, response = self.run_test(
            "Legal QA Stats - RAG System Statistics", 
            "GET", 
            "legal-qa/stats", 
            200
        )
        
        if success and isinstance(response, dict):
            # Check for expected statistics fields
            expected_fields = ['vector_db', 'embeddings_model', 'total_documents', 'last_updated']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Stats contain '{field}': {response[field]}")
                else:
                    print(f"   ⚠️  Stats missing '{field}' field")
            
            # Check specific values if available
            if 'vector_db' in response:
                vector_db = response['vector_db']
                if vector_db in ['supabase', 'chroma', 'pinecone']:
                    print(f"   ✅ Valid vector database: {vector_db}")
                else:
                    print(f"   ⚠️  Unknown vector database: {vector_db}")
            
            if 'total_documents' in response:
                doc_count = response['total_documents']
                if doc_count > 0:
                    print(f"   ✅ Knowledge base has {doc_count} documents")
                else:
                    print(f"   ⚠️  Knowledge base appears empty (0 documents)")
                    
        return success, response

    def test_legal_qa_knowledge_base_stats(self):
        """Test GET /api/legal-qa/knowledge-base/stats - Knowledge base statistics"""
        success, response = self.run_test(
            "Legal QA Knowledge Base Stats", 
            "GET", 
            "legal-qa/knowledge-base/stats", 
            200
        )
        
        if success and isinstance(response, dict):
            # Check for expected knowledge base fields
            expected_fields = ['total_documents', 'jurisdictions', 'legal_domains', 'last_updated']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Knowledge base stats contain '{field}'")
                    if field == 'jurisdictions' and isinstance(response[field], list):
                        print(f"     - Jurisdictions: {response[field]}")
                    elif field == 'legal_domains' and isinstance(response[field], list):
                        print(f"     - Legal domains: {response[field]}")
                    elif field == 'total_documents':
                        print(f"     - Total documents: {response[field]}")
                else:
                    print(f"   ⚠️  Knowledge base stats missing '{field}' field")
            
            # Validate data quality
            total_docs = response.get('total_documents', 0)
            jurisdictions = response.get('jurisdictions', [])
            legal_domains = response.get('legal_domains', [])
            
            if total_docs > 100:
                print(f"   ✅ Substantial knowledge base with {total_docs} documents")
            elif total_docs > 0:
                print(f"   ⚠️  Small knowledge base with {total_docs} documents")
            else:
                print(f"   ❌ Empty knowledge base")
            
            if len(jurisdictions) >= 5:
                print(f"   ✅ Good jurisdiction coverage: {len(jurisdictions)} jurisdictions")
            else:
                print(f"   ⚠️  Limited jurisdiction coverage: {len(jurisdictions)} jurisdictions")
            
            if len(legal_domains) >= 8:
                print(f"   ✅ Good legal domain coverage: {len(legal_domains)} domains")
            else:
                print(f"   ⚠️  Limited legal domain coverage: {len(legal_domains)} domains")
                
        return success, response

    def test_legal_qa_conversation_retrieval(self):
        """Test GET /api/legal-qa/conversation/{session_id} - Conversation history retrieval"""
        success, response = self.run_test(
            f"Legal QA Conversation Retrieval - Session {self.session_id[:8]}...", 
            "GET", 
            f"legal-qa/conversation/{self.session_id}", 
            200
        )
        
        if success and isinstance(response, dict):
            # Check response structure
            expected_fields = ['session_id', 'messages', 'created_at', 'last_updated']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Conversation contains '{field}' field")
                else:
                    print(f"   ⚠️  Conversation missing '{field}' field")
            
            # Check session ID match
            returned_session_id = response.get('session_id')
            if returned_session_id == self.session_id:
                print(f"   ✅ Session ID matches request")
            else:
                print(f"   ⚠️  Session ID mismatch")
            
            # Check messages
            messages = response.get('messages', [])
            if messages:
                print(f"   ✅ Found {len(messages)} messages in conversation history")
                for i, message in enumerate(messages[:2]):  # Show first 2 messages
                    msg_type = message.get('type', 'unknown')
                    content = message.get('content', '')[:100]
                    print(f"     - Message {i+1} ({msg_type}): {content}...")
            else:
                print(f"   ⚠️  No messages found in conversation history")
                
        return success, response

    def test_legal_qa_conversation_clear(self):
        """Test DELETE /api/legal-qa/conversation/{session_id} - Clear conversation history"""
        # Create a new session ID for this test to avoid affecting other tests
        clear_session_id = str(uuid.uuid4())
        
        # First, create some conversation history
        ask_data = {
            "question": "What is a contract?",
            "session_id": clear_session_id
        }
        
        # Ask a question to create conversation history
        create_success, create_response = self.run_test(
            "Create Conversation for Clear Test", 
            "POST", 
            "legal-qa/ask", 
            200, 
            ask_data,
            timeout=60
        )
        
        if not create_success:
            print("   ⚠️  Could not create conversation history for clear test")
            return False, {}
        
        # Now test clearing the conversation
        success, response = self.run_test(
            f"Legal QA Clear Conversation - Session {clear_session_id[:8]}...", 
            "DELETE", 
            f"legal-qa/conversation/{clear_session_id}", 
            200
        )
        
        if success:
            # Verify the conversation was cleared by trying to retrieve it
            verify_success, verify_response = self.run_test(
                "Verify Conversation Cleared", 
                "GET", 
                f"legal-qa/conversation/{clear_session_id}", 
                404  # Should return 404 if conversation was cleared
            )
            
            if verify_success:
                print(f"   ✅ Conversation successfully cleared - returns 404 on retrieval")
            else:
                print(f"   ⚠️  Conversation may not have been fully cleared")
                
        return success, response

    def test_legal_qa_rebuild_knowledge_base(self):
        """Test POST /api/legal-qa/rebuild-knowledge-base - Standard knowledge base rebuild"""
        rebuild_data = {
            "collection_mode": "standard",
            "force_rebuild": False
        }
        
        success, response = self.run_test(
            "Legal QA Rebuild Knowledge Base - Standard Mode", 
            "POST", 
            "legal-qa/rebuild-knowledge-base", 
            200, 
            rebuild_data,
            timeout=300  # 5 minutes for rebuild operations
        )
        
        if success and isinstance(response, dict):
            # Check response structure
            expected_fields = ['status', 'message', 'collection_mode', 'estimated_time']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Rebuild response contains '{field}': {response[field]}")
                else:
                    print(f"   ⚠️  Rebuild response missing '{field}' field")
            
            # Check status
            status = response.get('status')
            if status in ['started', 'in_progress', 'completed']:
                print(f"   ✅ Valid rebuild status: {status}")
            else:
                print(f"   ⚠️  Unexpected rebuild status: {status}")
            
            # Check collection mode
            collection_mode = response.get('collection_mode')
            if collection_mode == 'standard':
                print(f"   ✅ Correct collection mode: {collection_mode}")
            else:
                print(f"   ⚠️  Unexpected collection mode: {collection_mode}")
                
        return success, response

    def test_legal_qa_rebuild_bulk_knowledge_base(self):
        """Test POST /api/legal-qa/rebuild-bulk-knowledge-base - Bulk knowledge base rebuild"""
        bulk_rebuild_data = {
            "target_documents": 15000,
            "quality_filters": True,
            "court_hierarchy": True
        }
        
        success, response = self.run_test(
            "Legal QA Rebuild Bulk Knowledge Base", 
            "POST", 
            "legal-qa/rebuild-bulk-knowledge-base", 
            200, 
            bulk_rebuild_data,
            timeout=300  # 5 minutes for bulk rebuild operations
        )
        
        if success and isinstance(response, dict):
            # Check response structure for bulk operations
            expected_fields = ['status', 'message', 'collection_mode', 'target_documents', 'features_enabled']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Bulk rebuild response contains '{field}'")
                    if field == 'target_documents':
                        print(f"     - Target documents: {response[field]}")
                    elif field == 'features_enabled' and isinstance(response[field], list):
                        print(f"     - Features enabled: {response[field]}")
                else:
                    print(f"   ⚠️  Bulk rebuild response missing '{field}' field")
            
            # Check bulk-specific features
            features = response.get('features_enabled', [])
            expected_features = ['pagination', 'quality_filters', 'court_hierarchy', 'rate_limiting']
            for feature in expected_features:
                if feature in features:
                    print(f"   ✅ Bulk feature enabled: {feature}")
                else:
                    print(f"   ⚠️  Bulk feature not mentioned: {feature}")
                    
        return success, response

    def test_legal_qa_rebuild_federal_resources(self):
        """Test POST /api/legal-qa/rebuild-federal-resources-knowledge-base - Federal resources rebuild"""
        federal_rebuild_data = {
            "include_supreme_court": True,
            "include_circuit_courts": True,
            "include_district_courts": False,
            "date_range": {
                "start": "2020-01-01",
                "end": "2025-01-01"
            }
        }
        
        success, response = self.run_test(
            "Legal QA Rebuild Federal Resources Knowledge Base", 
            "POST", 
            "legal-qa/rebuild-federal-resources-knowledge-base", 
            200, 
            federal_rebuild_data,
            timeout=300
        )
        
        if success and isinstance(response, dict):
            # Check federal-specific response fields
            expected_fields = ['status', 'message', 'court_levels', 'date_range']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Federal rebuild response contains '{field}'")
                else:
                    print(f"   ⚠️  Federal rebuild response missing '{field}' field")
            
            # Check court levels
            court_levels = response.get('court_levels', [])
            if 'supreme_court' in court_levels:
                print(f"   ✅ Supreme Court included in rebuild")
            if 'circuit_courts' in court_levels:
                print(f"   ✅ Circuit Courts included in rebuild")
                
        return success, response

    def test_legal_qa_rebuild_academic_knowledge_base(self):
        """Test POST /api/legal-qa/rebuild-academic-knowledge-base - Academic knowledge base rebuild"""
        academic_rebuild_data = {
            "include_law_reviews": True,
            "include_legal_journals": True,
            "include_case_studies": True,
            "academic_level": "graduate"
        }
        
        success, response = self.run_test(
            "Legal QA Rebuild Academic Knowledge Base", 
            "POST", 
            "legal-qa/rebuild-academic-knowledge-base", 
            200, 
            academic_rebuild_data,
            timeout=300
        )
        
        if success and isinstance(response, dict):
            # Check academic-specific response fields
            expected_fields = ['status', 'message', 'academic_sources', 'academic_level']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Academic rebuild response contains '{field}'")
                else:
                    print(f"   ⚠️  Academic rebuild response missing '{field}' field")
            
            # Check academic sources
            academic_sources = response.get('academic_sources', [])
            expected_sources = ['law_reviews', 'legal_journals', 'case_studies']
            for source in expected_sources:
                if source in academic_sources:
                    print(f"   ✅ Academic source included: {source}")
                else:
                    print(f"   ⚠️  Academic source not mentioned: {source}")
                    
        return success, response

    def test_legal_qa_complex_question(self):
        """Test complex legal question to verify RAG system functionality"""
        complex_question = "In a partnership agreement, what are the fiduciary duties of partners to each other, and how do these duties differ from those in a corporation between directors and shareholders?"
        
        complex_ask_data = {
            "question": complex_question,
            "session_id": self.session_id,
            "context": {
                "jurisdiction": "US",
                "contract_type": "partnership_agreement",
                "complexity": "high"
            }
        }
        
        success, response = self.run_test(
            "Legal QA Complex Question - Partnership Fiduciary Duties", 
            "POST", 
            "legal-qa/ask", 
            200, 
            complex_ask_data,
            timeout=120
        )
        
        if success and isinstance(response, dict):
            answer = response.get('answer', '')
            sources = response.get('sources', [])
            confidence = response.get('confidence', 0)
            
            print(f"   Complex question: {complex_question[:100]}...")
            print(f"   Answer length: {len(answer)} characters")
            print(f"   Sources found: {len(sources)}")
            print(f"   Confidence: {confidence}")
            
            # Check answer quality for complex question
            if len(answer) > 200:
                print(f"   ✅ Substantial answer provided for complex question")
            else:
                print(f"   ⚠️  Answer seems short for complex question")
            
            # Check for legal concepts in answer
            legal_concepts = ['fiduciary', 'duty', 'partnership', 'corporation', 'director', 'shareholder']
            found_concepts = [concept for concept in legal_concepts if concept.lower() in answer.lower()]
            
            if len(found_concepts) >= 4:
                print(f"   ✅ Answer contains relevant legal concepts: {found_concepts}")
            else:
                print(f"   ⚠️  Answer may lack legal depth. Found concepts: {found_concepts}")
            
            # Check source quality
            if len(sources) >= 3:
                print(f"   ✅ Good source coverage with {len(sources)} sources")
            else:
                print(f"   ⚠️  Limited source coverage with {len(sources)} sources")
                
        return success, response

    def run_all_tests(self):
        """Run all legal QA endpoint tests"""
        print("🚀 Starting Legal QA API Testing...")
        print(f"   Base URL: {self.base_url}")
        print(f"   API URL: {self.api_url}")
        print(f"   Session ID: {self.session_id}")
        print("=" * 80)
        
        # Test all endpoints in logical order
        test_results = {}
        
        # 1. Test basic RAG system statistics first
        test_results['stats'] = self.test_legal_qa_stats()
        test_results['knowledge_base_stats'] = self.test_legal_qa_knowledge_base_stats()
        
        # 2. Test question answering functionality
        test_results['ask_basic'] = self.test_legal_qa_ask()
        test_results['ask_complex'] = self.test_legal_qa_complex_question()
        
        # 3. Test conversation management
        test_results['conversation_retrieval'] = self.test_legal_qa_conversation_retrieval()
        test_results['conversation_clear'] = self.test_legal_qa_conversation_clear()
        
        # 4. Test knowledge base rebuild operations
        test_results['rebuild_standard'] = self.test_legal_qa_rebuild_knowledge_base()
        test_results['rebuild_bulk'] = self.test_legal_qa_rebuild_bulk_knowledge_base()
        test_results['rebuild_federal'] = self.test_legal_qa_rebuild_federal_resources()
        test_results['rebuild_academic'] = self.test_legal_qa_rebuild_academic_knowledge_base()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 LEGAL QA API TEST SUMMARY")
        print("=" * 80)
        
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        print("\n📋 DETAILED RESULTS:")
        
        # Categorize results
        working_endpoints = []
        failing_endpoints = []
        
        for test_name, (success, _) in test_results.items():
            if success:
                working_endpoints.append(test_name)
            else:
                failing_endpoints.append(test_name)
        
        if working_endpoints:
            print(f"\n✅ WORKING ENDPOINTS ({len(working_endpoints)}):")
            for endpoint in working_endpoints:
                print(f"   - {endpoint}")
        
        if failing_endpoints:
            print(f"\n❌ FAILING ENDPOINTS ({len(failing_endpoints)}):")
            for endpoint in failing_endpoints:
                print(f"   - {endpoint}")
        
        # Overall assessment
        if self.tests_passed == self.tests_run:
            print(f"\n🎉 ALL LEGAL QA ENDPOINTS WORKING PERFECTLY!")
            print(f"   ✅ No 502 Bad Gateway errors detected")
            print(f"   ✅ RAG system dependency issue resolved")
            print(f"   ✅ All endpoints return proper responses")
        elif self.tests_passed >= self.tests_run * 0.8:
            print(f"\n✅ LEGAL QA SYSTEM MOSTLY FUNCTIONAL")
            print(f"   ✅ Most endpoints working properly")
            print(f"   ⚠️  Some minor issues detected")
        else:
            print(f"\n❌ LEGAL QA SYSTEM HAS SIGNIFICANT ISSUES")
            print(f"   ❌ Multiple endpoints failing")
            print(f"   ❌ RAG system may still have dependency issues")
        
        return test_results

if __name__ == "__main__":
    tester = LegalQAAPITester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if tester.tests_passed == tester.tests_run:
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed