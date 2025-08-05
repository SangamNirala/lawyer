#!/usr/bin/env python3
"""
Focused Legal Repository Expansion
==================================

This script uses the existing sophisticated systems to quickly add
high-quality documents with focus on Supreme Court and federal cases.

Uses existing scripts:
- advanced_deep_legal_research.py
- comprehensive_legal_mining_system.py 
- maximum_repository_expansion.py

Target: Add 50,000+ documents quickly
"""

import asyncio
import logging
import json
import sys
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_advanced_research_focused():
    """Run advanced research with Supreme Court focus"""
    logger.info("🔍 Running Advanced Deep Legal Research (Supreme Court Focus)")
    
    try:
        # Import and initialize
        from advanced_deep_legal_research import AdvancedLegalResearchSystem
        
        system = AdvancedLegalResearchSystem()
        
        # Focus on Supreme Court expansion
        target = system.research_targets['supreme_court_expanded']
        target.target_count = 15000  # Reasonable target
        
        logger.info(f"📊 Target: {target.target_count:,} Supreme Court documents")
        
        # Execute focused research
        documents = await system.deep_courtlistener_mining(target)
        
        if documents:
            # Generate synthetic documents for additional coverage
            synthetic_docs = await system.comprehensive_synthetic_generation(target)
            documents.extend(synthetic_docs)
            
            logger.info(f"✅ Advanced research completed: {len(documents):,} documents")
            return len(documents)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Advanced research failed: {e}")
        return 0

async def run_comprehensive_mining_focused():
    """Run comprehensive legal mining with federal focus"""
    logger.info("⛏️ Running Comprehensive Legal Mining (Federal Focus)")
    
    try:
        # Import and initialize
        from comprehensive_legal_mining_system import ComprehensiveLegalMiner
        
        system = ComprehensiveLegalMiner()
        
        # Focus on federal court sources
        logger.info("📊 Targeting federal court documents")
        
        # Execute comprehensive mining
        await system.execute_comprehensive_mining()
        
        logger.info("✅ Comprehensive mining completed")
        return 1  # Success indicator
        
    except Exception as e:
        logger.error(f"❌ Comprehensive mining failed: {e}")
        return 0

def get_repository_stats():
    """Get current repository statistics"""
    repo_path = Path("/app/legal_documents_repository_organized")
    
    if not repo_path.exists():
        return 0
    
    return len(list(repo_path.rglob("*.json")))

async def quick_courtlistener_expansion():
    """Quick CourtListener expansion using existing API keys"""
    logger.info("⚖️ Quick CourtListener Expansion")
    
    try:
        import aiohttp
        import random
        from datetime import datetime
        
        # Use existing CourtListener keys
        api_keys = [
            'e7a714db2df7fb77b6065a9d69158dcb85fa1acd',
            '7ec22683a2adf0f192e3219df2a9bdbe6c5aaa4a',
            'cd364ff091a9aaef6a1989e054e2f8e215923f46',
            '9c48f847b58da0ee5a42d52d7cbcf022d07c5d96'
        ]
        
        # Supreme Court and federal queries
        queries = [
            'court:scotus AND constitutional',
            'court:scotus AND "due process"',
            'court:scotus AND "equal protection"',
            'court:scotus AND "first amendment"',
            'court:(ca1 OR ca2 OR ca3 OR ca4 OR ca5 OR ca6 OR ca7 OR ca8 OR ca9 OR ca10 OR ca11 OR cadc OR cafc) AND precedential',
            'court:(ca1 OR ca2 OR ca3 OR ca4 OR ca5 OR ca6 OR ca7 OR ca8 OR ca9 OR ca10 OR ca11 OR cadc OR cafc) AND "federal jurisdiction"'
        ]
        
        documents_collected = 0
        
        async with aiohttp.ClientSession() as session:
            for query in queries:
                try:
                    api_key = random.choice(api_keys)
                    url = "https://www.courtlistener.com/api/rest/v3/search/"
                    
                    params = {
                        'q': query,
                        'type': 'o',  # Opinions
                        'order_by': 'score desc',
                        'status': 'Precedential',
                        'filed_after': '2015-01-01',
                    }
                    
                    headers = {
                        'Authorization': f'Token {api_key}',
                        'User-Agent': 'FocusedLegalExpansion/1.0'
                    }
                    
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = data.get('results', [])
                            documents_collected += len(results)
                            
                            logger.info(f"   📥 Query '{query[:30]}...': {len(results)} results")
                        
                    await asyncio.sleep(2.0)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Query error: {e}")
                    continue
        
        logger.info(f"✅ CourtListener quick expansion: {documents_collected} documents identified")
        return documents_collected
        
    except Exception as e:
        logger.error(f"❌ Quick CourtListener expansion failed: {e}")
        return 0

async def main():
    """Main focused expansion function"""
    logger.info("🚀 FOCUSED LEGAL REPOSITORY EXPANSION")
    logger.info("=" * 60)
    logger.info("🎯 Target: High-quality Supreme Court and Federal Cases")
    logger.info("📊 Method: Use existing sophisticated systems")
    
    # Get initial stats
    initial_count = get_repository_stats()
    logger.info(f"📊 Initial repository: {initial_count:,} documents")
    
    start_time = datetime.now()
    results = {}
    
    # Phase 1: Quick CourtListener expansion
    logger.info(f"\n{'='*50}")
    logger.info("PHASE 1: Quick CourtListener Expansion")
    logger.info('='*50)
    
    results['courtlistener'] = await quick_courtlistener_expansion()
    
    # Phase 2: Advanced research system
    logger.info(f"\n{'='*50}")
    logger.info("PHASE 2: Advanced Deep Legal Research")
    logger.info('='*50)
    
    results['advanced_research'] = await run_advanced_research_focused()
    
    # Phase 3: Comprehensive mining
    logger.info(f"\n{'='*50}")
    logger.info("PHASE 3: Comprehensive Legal Mining")
    logger.info('='*50)
    
    results['comprehensive_mining'] = await run_comprehensive_mining_focused()
    
    # Final stats
    final_count = get_repository_stats()
    duration = datetime.now() - start_time
    documents_added = final_count - initial_count
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("FOCUSED EXPANSION COMPLETION SUMMARY")
    logger.info('='*60)
    
    logger.info(f"⏱️  Duration: {duration}")
    logger.info(f"📊 Initial: {initial_count:,} documents")
    logger.info(f"📊 Final: {final_count:,} documents")
    logger.info(f"📈 Added: {documents_added:,} documents")
    
    logger.info(f"\n📊 Phase Results:")
    for phase, result in results.items():
        logger.info(f"   {phase}: {result}")
    
    # Save summary
    summary = {
        "focused_expansion_summary": {
            "completion_date": datetime.now().isoformat(),
            "duration_seconds": duration.total_seconds(),
            "initial_documents": initial_count,
            "final_documents": final_count,
            "documents_added": documents_added,
            "success": documents_added > 0
        },
        "phase_results": results,
        "focus": "Supreme Court and Federal Cases",
        "method": "Existing sophisticated systems"
    }
    
    summary_file = Path("/app/legal_documents_repository_organized") / "focused_expansion_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    if documents_added > 0:
        logger.info(f"\n🎉 FOCUSED EXPANSION SUCCESSFUL!")
        logger.info(f"📚 Repository expanded to {final_count:,} documents")
        return True
    else:
        logger.error(f"\n❌ FOCUSED EXPANSION FAILED - No documents added")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        logger.info("\n⚠️ Expansion interrupted by user")
        sys.exit(2)
    except Exception as e:
        logger.error(f"\n💥 Expansion crashed: {e}")
        sys.exit(3)