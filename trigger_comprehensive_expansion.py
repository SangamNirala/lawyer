"""
Simple script to trigger the comprehensive repository expansion via API
"""

import requests
import json
import time
import os

def trigger_comprehensive_expansion():
    """Trigger the comprehensive repository expansion via API"""
    
    # Get backend URL from environment or use default
    backend_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
    endpoint = f"{backend_url}/api/legal-qa/comprehensive-repository-expansion"
    
    print("🚀 TRIGGERING COMPREHENSIVE REPOSITORY EXPANSION")
    print("=" * 80)
    print(f"API Endpoint: {endpoint}")
    print("Target: 100,000+ legal documents")
    print("Strategy: CourtListener + Web Research + Synthetic Generation")
    print("=" * 80)
    
    try:
        # Make POST request to trigger expansion
        print("📡 Sending expansion request...")
        response = requests.post(endpoint, timeout=7200)  # 2 hour timeout
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ EXPANSION COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"📊 Documents Added: {result.get('actual_documents_added', 'N/A'):,}")
            print(f"🎯 Target Achievement: {result.get('target_achievement_percentage', 'N/A')}")
            print(f"⏱️  Runtime: {result.get('runtime_hours', 'N/A')} hours")
            print(f"✅ Success: {result.get('success', False)}")
            
            # Phase breakdown
            print("\n📈 Phase Results:")
            phase_breakdown = result.get('phase_breakdown', {})
            for phase, info in phase_breakdown.items():
                if isinstance(info, dict):
                    print(f"  • {phase}: {info.get('documents', 0):,} documents (target: {info.get('target', 0):,})")
                else:
                    print(f"  • {phase}: {info:,} documents")
            
            # API performance
            api_perf = result.get('api_performance', {})
            if api_perf:
                print("\n🔄 API Performance:")
                print(f"  • CourtListener Keys Used: {api_perf.get('courtlistener_keys_used', 'N/A')}")
                print(f"  • Total API Requests: {api_perf.get('total_api_requests', 'N/A'):,}")
                print(f"  • API Failure Rate: {api_perf.get('api_failure_rate', 'N/A')}")
            
            # Source distribution
            source_dist = result.get('source_distribution', {})
            if source_dist:
                print("\n📚 Source Distribution:")
                for source, count in list(source_dist.items())[:10]:  # Top 10 sources
                    print(f"  • {source}: {count:,} documents")
            
            # Quality assurance
            qa = result.get('quality_assurance', {})
            if qa:
                print("\n🔍 Quality Assurance:")
                for feature, status in qa.items():
                    print(f"  • {feature}: {status}")
            
            # Next steps
            next_steps = result.get('next_steps', [])
            if next_steps:
                print("\n🚀 Next Steps:")
                for step in next_steps:
                    print(f"  • {step}")
            
            # Errors
            errors = result.get('errors', [])
            if errors:
                print(f"\n⚠️  Errors Encountered: {len(errors)}")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"  • {error}")
            
            print("\n🎉 Repository expansion completed successfully!")
            return True
            
        else:
            print(f"❌ Expansion failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out - expansion may still be running in background")
        print("Check the server logs for progress updates")
        return False
        
    except Exception as e:
        print(f"❌ Error triggering expansion: {e}")
        return False

if __name__ == "__main__":
    success = trigger_comprehensive_expansion()
    if success:
        print("\n✅ Expansion trigger completed successfully!")
    else:
        print("\n❌ Expansion trigger failed!")