#!/usr/bin/env python3
"""
Legal Repository Test Expansion
===============================

Quick test to verify the expansion system works correctly before full run.
"""

import asyncio
import logging
from pathlib import Path
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_harvard_cap_collection():
    """Test Harvard CAP collection with small sample"""
    logger.info("🧪 Testing Harvard CAP collection...")
    
    try:
        from enhanced_legal_expansion import EnhancedLegalExpansionSystem
        
        system = EnhancedLegalExpansionSystem()
        
        # Test with small count
        documents = await system.collect_from_harvard_cap(target_count=50)
        
        logger.info(f"✅ Harvard CAP test completed: {len(documents)} documents collected")
        
        if documents:
            sample_doc = documents[0]
            logger.info(f"📄 Sample document: {sample_doc['title'][:50]}...")
            logger.info(f"📊 Sample word count: {sample_doc['word_count']}")
            logger.info(f"⚖️ Sample court: {sample_doc['court']}")
        
        return len(documents)
        
    except Exception as e:
        logger.error(f"❌ Harvard CAP test failed: {e}")
        return 0

async def test_courtlistener_collection():
    """Test CourtListener collection with small sample"""
    logger.info("🧪 Testing CourtListener collection...")
    
    try:
        from enhanced_legal_expansion import EnhancedLegalExpansionSystem
        
        system = EnhancedLegalExpansionSystem()
        
        # Test with small count
        documents = await system.collect_from_enhanced_courtlistener(target_count=25)
        
        logger.info(f"✅ CourtListener test completed: {len(documents)} documents collected")
        
        if documents:
            sample_doc = documents[0]
            logger.info(f"📄 Sample document: {sample_doc['title'][:50]}...")
            logger.info(f"📊 Sample word count: {sample_doc['word_count']}")
            logger.info(f"⚖️ Sample court: {sample_doc['court']}")
        
        return len(documents)
        
    except Exception as e:
        logger.error(f"❌ CourtListener test failed: {e}")
        return 0

async def test_directory_structure():
    """Test intelligent directory structure"""
    logger.info("🧪 Testing directory structure...")
    
    try:
        from enhanced_legal_expansion import EnhancedLegalExpansionSystem
        
        system = EnhancedLegalExpansionSystem()
        
        # Create some test documents
        test_docs = []
        for i in range(10):
            doc = {
                "id": f"test_doc_{i}_{datetime.now().strftime('%Y%m%d')}",
                "title": f"Test Legal Document {i}",
                "content": f"This is test legal content for document {i}. " * 50,  # About 500 words
                "source": "Test Source",
                "jurisdiction": "us_federal",
                "legal_domain": "constitutional_law",
                "document_type": "case",
                "court": "Supreme Court",
                "citation": f"Test {i} F.3d 123 (2024)",
                "case_name": f"Test Case {i}",
                "date_filed": "2024-01-01",
                "judges": ["Judge Test"],
                "attorneys": [],
                "legal_topics": ["constitutional_law"],
                "precedential_status": "Published",
                "court_level": "supreme",
                "word_count": 500,
                "quality_score": 0.9,
                "metadata": {
                    "collection_date": datetime.now().isoformat(),
                    "test_document": True
                }
            }
            test_docs.append(doc)
        
        # Test directory structure creation
        grouped_docs = system.create_intelligent_directory_structure(test_docs)
        
        logger.info(f"✅ Directory structure test completed")
        logger.info(f"📁 Created {len(grouped_docs)} directory groups")
        for group_name, docs in grouped_docs.items():
            logger.info(f"   📂 {group_name}: {len(docs)} documents")
        
        return len(grouped_docs)
        
    except Exception as e:
        logger.error(f"❌ Directory structure test failed: {e}")
        return 0

async def run_quick_test():
    """Run quick test of all components"""
    logger.info("🚀 Starting Legal Repository Quick Test")
    logger.info("=" * 60)
    
    results = {}
    
    # Test Harvard CAP
    results['harvard_cap'] = await test_harvard_cap_collection()
    
    # Test CourtListener
    results['courtlistener'] = await test_courtlistener_collection()
    
    # Test directory structure
    results['directory_structure'] = await test_directory_structure()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("🧪 QUICK TEST RESULTS")
    logger.info("=" * 60)
    
    total_success = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result > 0 else "❌ FAIL"
        logger.info(f"{test_name}: {status} ({result} items)")
        if result > 0:
            total_success += 1
    
    logger.info(f"\n📊 Overall: {total_success}/{len(results)} tests passed")
    
    if total_success >= 2:  # At least 2 tests should pass
        logger.info("🎉 Quick test successful - system ready for full expansion!")
        return True
    else:
        logger.error("❌ Quick test failed - system needs debugging")
        return False

if __name__ == "__main__":
    result = asyncio.run(run_quick_test())
    print(f"\n{'✅ SUCCESS' if result else '❌ FAILURE'}: Quick test {'completed' if result else 'failed'}")