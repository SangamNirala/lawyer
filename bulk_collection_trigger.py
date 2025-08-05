#!/usr/bin/env python3
"""
Bulk Collection Trigger
======================

This script triggers the existing CourtListener bulk collection system
to fetch additional real legal documents from the CourtListener API.
"""

import requests
import json
import time
import sys
from datetime import datetime

def trigger_bulk_collection():
    """Trigger the bulk collection endpoint"""
    
    print("🚀 Triggering CourtListener Bulk Collection")
    print("=" * 50)
    
    # API endpoint
    url = "http://localhost:8001/api/legal-qa/rebuild-bulk-knowledge-base"
    
    try:
        print("📡 Sending request to bulk collection endpoint...")
        print(f"🌐 URL: {url}")
        
        # Make the request
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               timeout=600)  # 10 minute timeout
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Bulk collection started successfully!")
            print(f"📊 Response: {json.dumps(result, indent=2)}")
            
            # Extract key information
            if isinstance(result, dict):
                collection_mode = result.get('collection_mode', 'bulk')
                target_achievement = result.get('target_achievement', {})
                features_enabled = result.get('features_enabled', [])
                
                print(f"\n📋 Collection Details:")
                print(f"   Mode: {collection_mode}")
                print(f"   Target Achievement: {target_achievement}")
                print(f"   Features: {', '.join(features_enabled) if features_enabled else 'Standard features'}")
            
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - bulk collection may still be running in background")
        print("✅ This is normal for large collection operations")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server")
        print("🔧 Please ensure the backend is running on localhost:8001")
        
    except Exception as e:
        print(f"❌ Error triggering bulk collection: {e}")

def check_knowledge_base_stats():
    """Check current knowledge base statistics"""
    
    print("\n📊 Checking Knowledge Base Statistics")
    print("-" * 40)
    
    try:
        # Check general stats
        stats_url = "http://localhost:8001/api/legal-qa/stats"
        response = requests.get(stats_url, timeout=30)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Current Knowledge Base Stats:")
            print(f"📄 Vector DB: {stats.get('vector_db', 'Unknown')}")
            print(f"🧠 Embeddings Model: {stats.get('embeddings_model', 'Unknown')}")
            
        # Check knowledge base specific stats  
        kb_stats_url = "http://localhost:8001/api/legal-qa/knowledge-base/stats"
        response = requests.get(kb_stats_url, timeout=30)
        
        if response.status_code == 200:
            kb_stats = response.json()
            print(f"📊 Knowledge Base Documents: {kb_stats.get('total_documents', 'Unknown')}")
            
            jurisdictions = kb_stats.get('jurisdictions', {})
            domains = kb_stats.get('legal_domains', {})
            
            print(f"🌍 Jurisdictions: {len(jurisdictions)} ({', '.join(list(jurisdictions.keys())[:5])}{'...' if len(jurisdictions) > 5 else ''})")
            print(f"⚖️ Legal Domains: {len(domains)} ({', '.join(list(domains.keys())[:5])}{'...' if len(domains) > 5 else ''})")
            
    except Exception as e:
        print(f"❌ Could not retrieve knowledge base stats: {e}")

def main():
    """Main function"""
    print("🔄 Legal Repository Bulk Collection System")
    print("==========================================")
    
    # Check current stats
    check_knowledge_base_stats()
    
    # Trigger bulk collection
    trigger_bulk_collection()
    
    print("\n🎯 Next Steps:")
    print("1. The bulk collection will run in the background")
    print("2. Check the backend logs for detailed progress")
    print("3. Monitor the legal_documents_repository for new files")
    print("4. The synthetic document generator is also running")
    print("\n📈 Your repository will be significantly expanded with both:")
    print("   • Real legal documents from CourtListener API")
    print("   • High-quality synthetic legal documents")

if __name__ == "__main__":
    main()