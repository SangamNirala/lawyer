#!/usr/bin/env python3
"""
Legal Documents Repository Browser

This script provides an interactive way to browse and search 
the 25,000+ document legal repository.
"""

import json
import os
from pathlib import Path
from datetime import datetime

class LegalRepositoryBrowser:
    def __init__(self, repo_path="/app/legal_documents_repository"):
        self.repo_path = Path(repo_path)
        self.load_index()
    
    def load_index(self):
        """Load the repository index"""
        try:
            index_path = self.repo_path / "comprehensive_repository_index.json"
            with open(index_path, 'r') as f:
                self.index = json.load(f)
        except Exception as e:
            print(f"Error loading index: {e}")
            self.index = {}
    
    def show_repository_stats(self):
        """Display repository statistics"""
        print("=" * 60)
        print("📊 LEGAL DOCUMENTS REPOSITORY STATISTICS")
        print("=" * 60)
        
        repo_info = self.index.get("repository_info", {})
        print(f"📅 Created: {repo_info.get('created_at', 'Unknown')}")
        print(f"📚 Total Documents: {repo_info.get('total_documents', 0):,}")
        print(f"🎯 Target Achieved: {'✅ Yes' if repo_info.get('target_achieved') else '❌ No'}")
        print(f"🔧 Generation Method: {repo_info.get('generation_method', 'Unknown')}")
        print()
        
        # Category breakdown
        print("📁 DOCUMENTS BY CATEGORY:")
        print("-" * 30)
        by_category = self.index.get("document_statistics", {}).get("by_category", {})
        for category, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"   {category:25}: {count:,}")
        print()
        
        # Jurisdiction breakdown
        print("🌍 DOCUMENTS BY JURISDICTION:")
        print("-" * 30)
        by_jurisdiction = self.index.get("document_statistics", {}).get("by_jurisdiction", {})
        for jurisdiction, count in sorted(by_jurisdiction.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"   {jurisdiction:25}: {count:,}")
        print()
        
        # Legal domain breakdown
        print("⚖️  DOCUMENTS BY LEGAL DOMAIN:")
        print("-" * 30)
        by_domain = self.index.get("document_statistics", {}).get("by_legal_domain", {})
        for domain, count in sorted(by_domain.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"   {domain:25}: {count:,}")
        print()
    
    def browse_category(self, category=None):
        """Browse documents in a specific category"""
        if not category:
            print("📁 AVAILABLE CATEGORIES:")
            print("-" * 25)
            structure = self.index.get("directory_structure", {})
            for cat, subcats in structure.items():
                if isinstance(subcats, dict):
                    total = sum(subcats.values())
                    if total > 0:
                        print(f"   📁 {cat}: {total:,} documents")
            return
        
        category_path = self.repo_path / category
        if not category_path.exists():
            print(f"❌ Category '{category}' not found")
            return
        
        print(f"📁 BROWSING CATEGORY: {category}")
        print("-" * 40)
        
        for subcat_path in category_path.iterdir():
            if subcat_path.is_dir():
                json_files = list(subcat_path.glob("*.json"))
                doc_count = len(json_files)
                if doc_count > 0:
                    print(f"   📂 {subcat_path.name}: {doc_count:,} documents")
                    
                    # Show sample documents
                    print("      Sample documents:")
                    for json_file in json_files[:3]:
                        try:
                            with open(json_file, 'r') as f:
                                doc = json.load(f)
                            title = doc.get('title', 'Untitled')[:50] + '...'
                            print(f"         • {title}")
                        except Exception as e:
                            print(f"         • Error reading {json_file.name}")
                    print()
    
    def search_documents(self, search_term, max_results=10):
        """Search for documents containing specific terms"""
        print(f"🔍 SEARCHING FOR: '{search_term}'")
        print("-" * 40)
        
        results = []
        search_count = 0
        
        for json_file in self.repo_path.rglob("*.json"):
            if json_file.name in ["comprehensive_repository_index.json", "document_catalog.json"]:
                continue
            
            search_count += 1
            if search_count > 1000:  # Limit search to first 1000 files for speed
                break
            
            try:
                with open(json_file, 'r') as f:
                    doc = json.load(f)
                
                # Search in title and content
                title = doc.get('title', '').lower()
                content = doc.get('content', '').lower()
                
                if search_term.lower() in title or search_term.lower() in content:
                    results.append({
                        'file': json_file,
                        'doc': doc,
                        'relevance': title.count(search_term.lower()) * 2 + content.count(search_term.lower())
                    })
            
            except Exception as e:
                continue
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        print(f"📊 Found {len(results)} results (searched {search_count} documents)")
        print()
        
        for i, result in enumerate(results[:max_results]):
            doc = result['doc']
            print(f"{i+1}. 📄 {doc.get('title', 'Untitled')}")
            print(f"   🏛️  Court: {doc.get('court', 'N/A')}")
            print(f"   📍 Jurisdiction: {doc.get('jurisdiction', 'N/A')}")
            print(f"   ⚖️  Domain: {doc.get('legal_domain', 'N/A')}")
            print(f"   📁 File: {result['file'].relative_to(self.repo_path)}")
            print()
    
    def view_document(self, doc_path):
        """View a specific document"""
        full_path = self.repo_path / doc_path
        
        if not full_path.exists():
            print(f"❌ Document not found: {doc_path}")
            return
        
        try:
            with open(full_path, 'r') as f:
                doc = json.load(f)
            
            print("=" * 60)
            print("📄 DOCUMENT VIEWER")
            print("=" * 60)
            print(f"📋 Title: {doc.get('title', 'Untitled')}")
            print(f"🆔 ID: {doc.get('id', 'N/A')}")
            print(f"🏛️  Court: {doc.get('court', 'N/A')}")
            print(f"📍 Jurisdiction: {doc.get('jurisdiction', 'N/A')}")
            print(f"⚖️  Legal Domain: {doc.get('legal_domain', 'N/A')}")
            print(f"📅 Date Filed: {doc.get('date_filed', 'N/A')}")
            print(f"👨‍⚖️ Judges: {', '.join(doc.get('judges', []))}")
            print(f"📖 Citation: {doc.get('citation', 'N/A')}")
            print()
            print("📝 CONTENT:")
            print("-" * 20)
            content = doc.get('content', 'No content available')
            # Show first 1000 characters
            print(content[:1000] + ('...' if len(content) > 1000 else ''))
            print()
            
            if doc.get('precedents_cited'):
                print("📚 PRECEDENTS CITED:")
                for precedent in doc.get('precedents_cited', [])[:5]:
                    print(f"   • {precedent}")
                print()
            
            if doc.get('statutes_cited'):
                print("📜 STATUTES CITED:")
                for statute in doc.get('statutes_cited', []):
                    print(f"   • {statute}")
                print()
        
        except Exception as e:
            print(f"❌ Error viewing document: {e}")
    
    def show_featured_documents(self):
        """Show featured high-quality documents"""
        try:
            catalog_path = self.repo_path / "document_catalog.json"
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)
            
            featured = catalog.get('featured_documents', [])
            
            print("⭐ FEATURED DOCUMENTS (High Quality)")
            print("=" * 40)
            
            for i, doc in enumerate(featured[:10], 1):
                print(f"{i:2d}. 📄 {doc.get('title', 'Untitled')}")
                print(f"     📍 {doc.get('jurisdiction', 'N/A')} | ⚖️  {doc.get('legal_domain', 'N/A')}")
                print(f"     📁 {doc.get('file_path', 'N/A')}")
                print()
        
        except Exception as e:
            print(f"❌ Error loading featured documents: {e}")
    
    def interactive_menu(self):
        """Interactive menu for browsing"""
        while True:
            print("\n" + "=" * 60)
            print("🏛️  LEGAL DOCUMENTS REPOSITORY BROWSER")
            print("=" * 60)
            print("1. 📊 Show Repository Statistics")
            print("2. 📁 Browse by Category")
            print("3. 🔍 Search Documents")
            print("4. ⭐ View Featured Documents")
            print("5. 📄 View Specific Document")
            print("6. ❌ Exit")
            print()
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':
                self.show_repository_stats()
            elif choice == '2':
                print("\nAvailable categories:")
                self.browse_category()
                category = input("\nEnter category name to browse (or press Enter to skip): ").strip()
                if category:
                    self.browse_category(category)
            elif choice == '3':
                search_term = input("Enter search term: ").strip()
                if search_term:
                    self.search_documents(search_term)
            elif choice == '4':
                self.show_featured_documents()
            elif choice == '5':
                doc_path = input("Enter document path (e.g., federal_courts/supreme_court/filename.json): ").strip()
                if doc_path:
                    self.view_document(doc_path)
            elif choice == '6':
                print("👋 Thank you for using the Legal Repository Browser!")
                break
            else:
                print("❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    browser = LegalRepositoryBrowser()
    
    # Show welcome message and stats
    print("🎉 Welcome to the Legal Documents Repository Browser!")
    print(f"📚 Repository contains 25,000+ legal documents")
    print(f"📁 Location: /app/legal_documents_repository")
    
    # Show quick stats
    browser.show_repository_stats()
    
    # Start interactive menu
    browser.interactive_menu()

if __name__ == "__main__":
    main()