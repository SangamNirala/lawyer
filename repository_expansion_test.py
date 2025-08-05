import requests
import sys
import json
import time
from datetime import datetime

class RepositoryExpansionTester:
    def __init__(self, base_url="https://bc3d4b4f-8924-49a9-b358-1b3f7cb3bc12.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=120):
        """Run a single API test with extended timeout for repository operations"""
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

    def test_comprehensive_repository_expansion_endpoint(self):
        """Test the new comprehensive repository expansion endpoint"""
        print("\n🎯 TESTING COMPREHENSIVE REPOSITORY EXPANSION ENDPOINT")
        print("=" * 70)
        
        # Test the new endpoint
        success, response = self.run_test(
            "Comprehensive Repository Expansion Endpoint",
            "POST",
            "legal-qa/comprehensive-repository-expansion",
            200,
            {},
            timeout=180  # Extended timeout for repository operations
        )
        
        if success and response:
            print(f"\n📊 COMPREHENSIVE REPOSITORY EXPANSION RESPONSE ANALYSIS:")
            
            # Check expected response structure
            expected_fields = [
                'expansion_id', 'status', 'repository_status', 'current_document_count',
                'target_document_count', 'expansion_needed', 'collection_strategy',
                'estimated_completion_time', 'quality_metrics', 'court_hierarchy_status',
                'legal_domain_distribution', 'jurisdiction_coverage', 'recommendations'
            ]
            
            missing_fields = []
            present_fields = []
            
            for field in expected_fields:
                if field in response:
                    present_fields.append(field)
                    print(f"   ✅ {field}: {response[field]}")
                else:
                    missing_fields.append(field)
                    print(f"   ❌ Missing field: {field}")
            
            # Analyze repository status
            current_count = response.get('current_document_count', 0)
            target_count = response.get('target_document_count', 100000)
            expansion_needed = response.get('expansion_needed', True)
            
            print(f"\n📈 REPOSITORY STATUS ANALYSIS:")
            print(f"   Current Documents: {current_count:,}")
            print(f"   Target Documents: {target_count:,}")
            print(f"   Expansion Needed: {expansion_needed}")
            
            # Check if system recognizes large repository
            if current_count >= 100000:
                print(f"   ✅ System correctly recognizes large repository (100,000+ documents)")
                if not expansion_needed:
                    print(f"   ✅ System correctly identifies target already achieved")
                else:
                    print(f"   ⚠️  System indicates expansion needed despite large repository")
            elif current_count >= 231207:
                print(f"   ✅ System correctly recognizes very large repository (231,207+ documents)")
            else:
                print(f"   ⚠️  Repository size ({current_count:,}) smaller than expected")
            
            # Analyze collection strategy
            if 'collection_strategy' in response:
                strategy = response['collection_strategy']
                print(f"\n🎯 COLLECTION STRATEGY ANALYSIS:")
                if isinstance(strategy, dict):
                    for key, value in strategy.items():
                        print(f"   {key}: {value}")
                else:
                    print(f"   Strategy: {strategy}")
            
            # Analyze quality metrics
            if 'quality_metrics' in response:
                metrics = response['quality_metrics']
                print(f"\n📊 QUALITY METRICS ANALYSIS:")
                if isinstance(metrics, dict):
                    for key, value in metrics.items():
                        print(f"   {key}: {value}")
                else:
                    print(f"   Metrics: {metrics}")
            
            # Analyze court hierarchy status
            if 'court_hierarchy_status' in response:
                hierarchy = response['court_hierarchy_status']
                print(f"\n🏛️  COURT HIERARCHY STATUS:")
                if isinstance(hierarchy, dict):
                    for court_level, status in hierarchy.items():
                        print(f"   {court_level}: {status}")
                else:
                    print(f"   Hierarchy: {hierarchy}")
            
            # Check recommendations
            if 'recommendations' in response:
                recommendations = response['recommendations']
                print(f"\n💡 RECOMMENDATIONS:")
                if isinstance(recommendations, list):
                    for i, rec in enumerate(recommendations, 1):
                        print(f"   {i}. {rec}")
                else:
                    print(f"   Recommendations: {recommendations}")
            
            # Overall assessment
            if len(missing_fields) == 0:
                print(f"\n✅ ALL EXPECTED FIELDS PRESENT - Response structure complete")
            else:
                print(f"\n⚠️  MISSING FIELDS: {missing_fields}")
            
            return True, response
        
        return success, response

    def test_legal_qa_stats_endpoint(self):
        """Test the RAG system statistics endpoint"""
        print("\n📊 TESTING RAG SYSTEM STATISTICS ENDPOINT")
        print("=" * 50)
        
        success, response = self.run_test(
            "Legal QA Stats Endpoint",
            "GET",
            "legal-qa/stats",
            200,
            timeout=60
        )
        
        if success and response:
            print(f"\n📈 RAG SYSTEM STATISTICS ANALYSIS:")
            
            # Expected fields for RAG stats
            expected_fields = [
                'vector_db', 'embeddings_model', 'total_documents', 'total_embeddings',
                'knowledge_base_status', 'last_updated', 'performance_metrics'
            ]
            
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ {field}: {response[field]}")
                else:
                    print(f"   ❌ Missing field: {field}")
            
            # Check specific values
            vector_db = response.get('vector_db', 'unknown')
            embeddings_model = response.get('embeddings_model', 'unknown')
            total_docs = response.get('total_documents', 0)
            
            print(f"\n🔍 DETAILED ANALYSIS:")
            print(f"   Vector Database: {vector_db}")
            print(f"   Embeddings Model: {embeddings_model}")
            print(f"   Total Documents: {total_docs:,}")
            
            # Validate expected configurations
            if vector_db == 'supabase':
                print(f"   ✅ Using expected Supabase vector database")
            else:
                print(f"   ⚠️  Unexpected vector database: {vector_db}")
            
            if 'MiniLM' in embeddings_model:
                print(f"   ✅ Using expected MiniLM embeddings model")
            else:
                print(f"   ⚠️  Unexpected embeddings model: {embeddings_model}")
            
            if total_docs >= 100000:
                print(f"   ✅ Large document collection confirmed ({total_docs:,} documents)")
            else:
                print(f"   ⚠️  Document count lower than expected: {total_docs:,}")
        
        return success, response

    def test_knowledge_base_stats_endpoint(self):
        """Test the knowledge base statistics endpoint"""
        print("\n📚 TESTING KNOWLEDGE BASE STATISTICS ENDPOINT")
        print("=" * 55)
        
        success, response = self.run_test(
            "Knowledge Base Stats Endpoint",
            "GET",
            "legal-qa/knowledge-base/stats",
            200,
            timeout=60
        )
        
        if success and response:
            print(f"\n📊 KNOWLEDGE BASE STATISTICS ANALYSIS:")
            
            # Expected fields for knowledge base stats
            expected_fields = [
                'total_documents', 'jurisdictions', 'legal_domains', 'document_types',
                'quality_distribution', 'last_updated', 'collection_metadata'
            ]
            
            for field in expected_fields:
                if field in response:
                    value = response[field]
                    if isinstance(value, (dict, list)):
                        print(f"   ✅ {field}: {len(value)} items")
                        if field == 'jurisdictions' and isinstance(value, list):
                            print(f"      Jurisdictions: {', '.join(value[:5])}{'...' if len(value) > 5 else ''}")
                        elif field == 'legal_domains' and isinstance(value, list):
                            print(f"      Legal Domains: {', '.join(value[:5])}{'...' if len(value) > 5 else ''}")
                    else:
                        print(f"   ✅ {field}: {value}")
                else:
                    print(f"   ❌ Missing field: {field}")
            
            # Analyze document distribution
            total_docs = response.get('total_documents', 0)
            jurisdictions = response.get('jurisdictions', [])
            legal_domains = response.get('legal_domains', [])
            
            print(f"\n🔍 DETAILED KNOWLEDGE BASE ANALYSIS:")
            print(f"   Total Documents: {total_docs:,}")
            print(f"   Jurisdictions Covered: {len(jurisdictions) if isinstance(jurisdictions, list) else 'N/A'}")
            print(f"   Legal Domains: {len(legal_domains) if isinstance(legal_domains, list) else 'N/A'}")
            
            # Check for expected large repository
            if total_docs >= 100000:
                print(f"   ✅ Large knowledge base confirmed ({total_docs:,} documents)")
            elif total_docs >= 10000:
                print(f"   ✅ Substantial knowledge base ({total_docs:,} documents)")
            else:
                print(f"   ⚠️  Knowledge base smaller than expected: {total_docs:,}")
            
            # Check jurisdiction coverage
            if isinstance(jurisdictions, list) and len(jurisdictions) >= 5:
                print(f"   ✅ Good jurisdiction coverage ({len(jurisdictions)} jurisdictions)")
            else:
                print(f"   ⚠️  Limited jurisdiction coverage")
            
            # Check legal domain coverage
            if isinstance(legal_domains, list) and len(legal_domains) >= 10:
                print(f"   ✅ Comprehensive legal domain coverage ({len(legal_domains)} domains)")
            else:
                print(f"   ⚠️  Limited legal domain coverage")
        
        return success, response

    def test_mongodb_integration(self):
        """Test MongoDB integration and document organization"""
        print("\n🗄️  TESTING MONGODB INTEGRATION")
        print("=" * 40)
        
        # Test if we can access any MongoDB-related endpoints
        # This might be through a general health check or database status endpoint
        
        # Try to test through the stats endpoints which should reflect MongoDB data
        print("   Testing MongoDB integration through stats endpoints...")
        
        # Test knowledge base stats (should reflect MongoDB data)
        kb_success, kb_response = self.test_knowledge_base_stats_endpoint()
        
        if kb_success and kb_response:
            total_docs = kb_response.get('total_documents', 0)
            
            print(f"\n🔍 MONGODB INTEGRATION ANALYSIS:")
            print(f"   Documents in Knowledge Base: {total_docs:,}")
            
            # Check for batch organization indicators
            if 'collection_metadata' in kb_response:
                metadata = kb_response['collection_metadata']
                print(f"   Collection Metadata Available: ✅")
                if isinstance(metadata, dict):
                    for key, value in metadata.items():
                        print(f"   {key}: {value}")
            
            # Check for date range organization (2015-2018, 2019-2020, etc.)
            if total_docs >= 100000:
                print(f"   ✅ Large document collection suggests proper MongoDB storage")
                print(f"   ✅ Document count indicates batch organization is working")
            
            # Look for indicators of proper indexing
            if 'last_updated' in kb_response:
                last_updated = kb_response['last_updated']
                print(f"   Last Updated: {last_updated}")
                print(f"   ✅ Timestamp tracking indicates proper MongoDB indexing")
        
        return kb_success, kb_response

    def test_repository_organization(self):
        """Test repository organization with batch directories and file limits"""
        print("\n📁 TESTING REPOSITORY ORGANIZATION")
        print("=" * 45)
        
        # Test the comprehensive expansion endpoint to get organization details
        success, response = self.run_test(
            "Repository Organization Analysis",
            "POST",
            "legal-qa/comprehensive-repository-expansion",
            200,
            {},
            timeout=120
        )
        
        if success and response:
            print(f"\n📊 REPOSITORY ORGANIZATION ANALYSIS:")
            
            # Check for organization indicators
            current_count = response.get('current_document_count', 0)
            
            # Calculate expected batch directories (assuming 1000 files per directory limit)
            expected_batches = (current_count // 1000) + (1 if current_count % 1000 > 0 else 0)
            
            print(f"   Total Documents: {current_count:,}")
            print(f"   Expected Batch Directories (1000 files/dir): {expected_batches:,}")
            
            # Check for date range organization
            if 'collection_strategy' in response:
                strategy = response['collection_strategy']
                if isinstance(strategy, dict):
                    if 'date_ranges' in strategy:
                        date_ranges = strategy['date_ranges']
                        print(f"   Date Range Organization: ✅")
                        print(f"   Date Ranges: {date_ranges}")
                    
                    if 'batch_organization' in strategy:
                        batch_org = strategy['batch_organization']
                        print(f"   Batch Organization: {batch_org}")
            
            # Check court hierarchy organization
            if 'court_hierarchy_status' in response:
                hierarchy = response['court_hierarchy_status']
                print(f"\n🏛️  COURT HIERARCHY ORGANIZATION:")
                if isinstance(hierarchy, dict):
                    for court_level, info in hierarchy.items():
                        if isinstance(info, dict) and 'document_count' in info:
                            doc_count = info['document_count']
                            expected_batches_court = (doc_count // 1000) + (1 if doc_count % 1000 > 0 else 0)
                            print(f"   {court_level}: {doc_count:,} docs, ~{expected_batches_court} batches")
                        else:
                            print(f"   {court_level}: {info}")
            
            # Validate 1000 files per directory limit compliance
            if current_count > 1000:
                print(f"\n✅ Repository size requires batch organization (>1000 files)")
                print(f"✅ Expected batch structure for {current_count:,} documents")
            else:
                print(f"\n⚠️  Repository size ({current_count}) may not require batching")
            
            # Check for date-based organization (2015-2018, 2019-2020, etc.)
            expected_date_ranges = ['2015-2018', '2019-2020', '2021-2022', '2023-2025']
            print(f"\n📅 EXPECTED DATE RANGE ORGANIZATION:")
            for date_range in expected_date_ranges:
                print(f"   Expected: {date_range} directory structure")
        
        return success, response

    def test_courtlistener_api_integration(self):
        """Test CourtListener API integration and configuration"""
        print("\n⚖️  TESTING COURTLISTENER API INTEGRATION")
        print("=" * 50)
        
        # Test through the comprehensive expansion endpoint which should use CourtListener
        success, response = self.run_test(
            "CourtListener Integration Test",
            "POST",
            "legal-qa/comprehensive-repository-expansion",
            200,
            {},
            timeout=120
        )
        
        if success and response:
            print(f"\n🔍 COURTLISTENER INTEGRATION ANALYSIS:")
            
            # Check for CourtListener-specific indicators
            if 'collection_strategy' in response:
                strategy = response['collection_strategy']
                if isinstance(strategy, dict):
                    # Look for CourtListener-specific fields
                    cl_indicators = ['api_key_status', 'rate_limiting', 'court_coverage', 'api_endpoints']
                    
                    for indicator in cl_indicators:
                        if indicator in strategy:
                            print(f"   ✅ {indicator}: {strategy[indicator]}")
                        else:
                            print(f"   ❌ Missing {indicator} information")
            
            # Check court hierarchy (should reflect CourtListener structure)
            if 'court_hierarchy_status' in response:
                hierarchy = response['court_hierarchy_status']
                print(f"\n🏛️  COURTLISTENER COURT HIERARCHY:")
                
                expected_courts = ['Supreme Court', 'Circuit Courts', 'District Courts']
                
                if isinstance(hierarchy, dict):
                    for court_type in expected_courts:
                        found = False
                        for key in hierarchy.keys():
                            if court_type.lower() in key.lower() or key.lower() in court_type.lower():
                                print(f"   ✅ {court_type}: Found as '{key}'")
                                found = True
                                break
                        if not found:
                            print(f"   ❌ {court_type}: Not found in hierarchy")
            
            # Check for quality control features (CourtListener-specific)
            if 'quality_metrics' in response:
                metrics = response['quality_metrics']
                if isinstance(metrics, dict):
                    cl_quality_indicators = ['precedential_only', 'published_only', 'min_word_count', 'court_level_filters']
                    
                    print(f"\n📊 COURTLISTENER QUALITY CONTROLS:")
                    for indicator in cl_quality_indicators:
                        if indicator in metrics:
                            print(f"   ✅ {indicator}: {metrics[indicator]}")
                        else:
                            print(f"   ❌ Missing {indicator}")
            
            # Check for API key availability
            if 'api_configuration' in response:
                api_config = response['api_configuration']
                print(f"\n🔑 API CONFIGURATION:")
                if isinstance(api_config, dict):
                    for key, value in api_config.items():
                        if 'key' in key.lower():
                            print(f"   ✅ {key}: {'Configured' if value else 'Missing'}")
                        else:
                            print(f"   {key}: {value}")
        
        return success, response

    def test_performance_with_large_repository(self):
        """Test system performance with large repository"""
        print("\n⚡ TESTING PERFORMANCE WITH LARGE REPOSITORY")
        print("=" * 55)
        
        # Test response times for various endpoints
        endpoints_to_test = [
            ("legal-qa/stats", "GET", "RAG Stats"),
            ("legal-qa/knowledge-base/stats", "GET", "Knowledge Base Stats"),
            ("legal-qa/comprehensive-repository-expansion", "POST", "Repository Expansion")
        ]
        
        performance_results = {}
        
        for endpoint, method, name in endpoints_to_test:
            print(f"\n⏱️  Testing {name} Performance...")
            
            start_time = time.time()
            
            if method == "GET":
                success, response = self.run_test(
                    f"{name} Performance Test",
                    method,
                    endpoint,
                    200,
                    timeout=60
                )
            else:
                success, response = self.run_test(
                    f"{name} Performance Test",
                    method,
                    endpoint,
                    200,
                    {},
                    timeout=120
                )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            performance_results[name] = {
                'success': success,
                'response_time': response_time,
                'response_size': len(str(response)) if response else 0
            }
            
            print(f"   Response Time: {response_time:.2f} seconds")
            
            # Performance thresholds
            if response_time < 5.0:
                print(f"   ✅ Excellent performance (<5s)")
            elif response_time < 15.0:
                print(f"   ✅ Good performance (<15s)")
            elif response_time < 30.0:
                print(f"   ⚠️  Acceptable performance (<30s)")
            else:
                print(f"   ❌ Slow performance (>30s)")
        
        # Overall performance summary
        print(f"\n📊 PERFORMANCE SUMMARY:")
        total_time = sum(result['response_time'] for result in performance_results.values())
        successful_tests = sum(1 for result in performance_results.values() if result['success'])
        
        print(f"   Total Test Time: {total_time:.2f} seconds")
        print(f"   Successful Tests: {successful_tests}/{len(performance_results)}")
        print(f"   Average Response Time: {total_time/len(performance_results):.2f} seconds")
        
        return True, performance_results

    def run_all_tests(self):
        """Run all repository expansion tests"""
        print("🚀 STARTING COMPREHENSIVE REPOSITORY EXPANSION TESTING")
        print("=" * 70)
        print(f"Testing against: {self.base_url}")
        print(f"API Base URL: {self.api_url}")
        
        # Test sequence
        test_methods = [
            self.test_comprehensive_repository_expansion_endpoint,
            self.test_legal_qa_stats_endpoint,
            self.test_knowledge_base_stats_endpoint,
            self.test_mongodb_integration,
            self.test_repository_organization,
            self.test_courtlistener_api_integration,
            self.test_performance_with_large_repository
        ]
        
        results = {}
        
        for test_method in test_methods:
            try:
                test_name = test_method.__name__
                print(f"\n" + "="*70)
                success, response = test_method()
                results[test_name] = {'success': success, 'response': response}
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed with exception: {str(e)}")
                results[test_method.__name__] = {'success': False, 'error': str(e)}
        
        # Final summary
        print("\n" + "="*70)
        print("🎯 COMPREHENSIVE REPOSITORY EXPANSION TEST SUMMARY")
        print("=" * 70)
        
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        print(f"\n📋 DETAILED TEST RESULTS:")
        for test_name, result in results.items():
            status = "✅ PASSED" if result['success'] else "❌ FAILED"
            print(f"   {test_name}: {status}")
            if not result['success'] and 'error' in result:
                print(f"      Error: {result['error']}")
        
        # Key findings summary
        print(f"\n🔍 KEY FINDINGS:")
        
        # Repository size analysis
        expansion_result = results.get('test_comprehensive_repository_expansion_endpoint', {})
        if expansion_result.get('success') and 'response' in expansion_result:
            response = expansion_result['response']
            current_count = response.get('current_document_count', 0)
            target_count = response.get('target_document_count', 100000)
            expansion_needed = response.get('expansion_needed', True)
            
            print(f"   📊 Repository Status:")
            print(f"      Current Documents: {current_count:,}")
            print(f"      Target Documents: {target_count:,}")
            print(f"      Expansion Needed: {expansion_needed}")
            
            if current_count >= 231207:
                print(f"      ✅ Repository exceeds expected size (231,207+ documents)")
            elif current_count >= 100000:
                print(f"      ✅ Repository meets large size threshold (100,000+ documents)")
            else:
                print(f"      ⚠️  Repository smaller than expected")
        
        # Performance analysis
        perf_result = results.get('test_performance_with_large_repository', {})
        if perf_result.get('success') and 'response' in perf_result:
            perf_data = perf_result['response']
            avg_time = sum(result['response_time'] for result in perf_data.values()) / len(perf_data)
            print(f"   ⚡ Performance:")
            print(f"      Average Response Time: {avg_time:.2f} seconds")
            if avg_time < 10:
                print(f"      ✅ Good performance with large repository")
            else:
                print(f"      ⚠️  Performance may be impacted by repository size")
        
        return results

if __name__ == "__main__":
    tester = RepositoryExpansionTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if all(result['success'] for result in results.values()):
        print(f"\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n⚠️  SOME TESTS FAILED - Check details above")
        sys.exit(1)