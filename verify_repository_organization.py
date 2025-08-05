#!/usr/bin/env python3
"""
Repository Organization Verification Script
==========================================

This script verifies that the legal documents repository organization 
complies with GitHub's directory display limits.
"""

import os
from pathlib import Path
from collections import defaultdict

def verify_repository_organization(repo_path="/app/legal_documents_repository_organized"):
    """Verify the organization meets GitHub directory limits"""
    repo_path = Path(repo_path)
    
    print("🔍 Verifying Legal Documents Repository Organization")
    print("=" * 60)
    
    violations = []
    directory_stats = defaultdict(int)
    total_files = 0
    total_directories = 0
    
    # Walk through all directories
    for root, dirs, files in os.walk(repo_path):
        json_files = [f for f in files if f.endswith('.json')]
        file_count = len(json_files)
        
        if json_files:  # Only count directories with JSON files
            total_directories += 1
            directory_stats[file_count] += 1
            total_files += file_count
            
            # Check for violations
            if file_count > 999:
                violations.append((root, file_count))
                
            # Show directory details
            rel_path = os.path.relpath(root, repo_path)
            if file_count > 0:
                status = "✅" if file_count <= 999 else "❌"
                print(f"{status} {rel_path}: {file_count} files")
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    print(f"📁 Total directories with JSON files: {total_directories}")
    print(f"📄 Total JSON files: {total_files:,}")
    print(f"🚫 Violations (>999 files): {len(violations)}")
    
    if violations:
        print(f"\n❌ VIOLATIONS FOUND:")
        for path, count in violations:
            print(f"   {path}: {count} files")
    else:
        print(f"\n✅ ALL DIRECTORIES COMPLY WITH GITHUB LIMITS!")
    
    print(f"\n📈 File Distribution:")
    for file_count in sorted(directory_stats.keys(), reverse=True):
        dir_count = directory_stats[file_count]
        print(f"   {file_count} files: {dir_count} directories")
    
    return len(violations) == 0

if __name__ == "__main__":
    is_valid = verify_repository_organization()
    print(f"\n🎯 Organization Status: {'VALID' if is_valid else 'INVALID'}")
    exit(0 if is_valid else 1)