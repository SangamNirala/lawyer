#!/usr/bin/env python3
"""
Legal Documents Repository Reorganizer
=====================================

This script reorganizes the legal_documents_repository from a structure that has directories 
with >1000 files (causing GitHub display issues) to a date-based structure where each 
directory contains ≤999 files.

Organization Strategy:
- Primary: Date-based folders (e.g., 2020-2021/, 2022-2023/, etc.)
- Secondary: Document type subfolders within date ranges
- Tertiary: Batch folders (batch_001/, batch_002/) if needed to keep under 999 files per folder

Author: Legal Repository Organizer
Date: January 2025
"""

import os
import json
import shutil
from datetime import datetime
from collections import defaultdict, Counter
import re
from pathlib import Path

class LegalRepositoryReorganizer:
    def __init__(self, source_dir="/app/legal_documents_repository", target_dir="/app/legal_documents_repository_organized"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.max_files_per_dir = 999
        self.file_stats = defaultdict(list)
        self.date_distribution = Counter()
        self.processed_files = 0
        self.skipped_files = 0
        
    def extract_date_from_file(self, file_path):
        """Extract date from JSON file's date_filed field or filename"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                date_filed = data.get('date_filed', '')
                if date_filed:
                    # Parse date in format YYYY-MM-DD
                    date_obj = datetime.strptime(date_filed, '%Y-%m-%d')
                    return date_obj.year
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            pass
            
        # Fallback: extract date from filename pattern (e.g., _20250805)
        filename = Path(file_path).name
        date_match = re.search(r'_(\d{8})', filename)
        if date_match:
            date_str = date_match.group(1)
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                return date_obj.year
            except ValueError:
                pass
                
        # Final fallback: use current year
        return 2024
    
    def get_document_type(self, file_path):
        """Determine document type from path and content"""
        path_str = str(file_path).lower()
        
        if 'supreme_court' in path_str:
            return 'supreme_court'
        elif 'circuit_courts' in path_str:
            return 'circuit_courts'
        elif 'district_courts' in path_str:
            return 'district_courts'
        elif 'regulations' in path_str:
            return 'regulations'
        elif 'statutes' in path_str:
            return 'statutes'
        elif 'academic' in path_str:
            return 'academic'
        elif 'state_courts' in path_str:
            return 'state_courts'
        elif 'constitutional_law' in path_str:
            return 'constitutional_law'
        elif 'contracts' in path_str:
            return 'contracts'
        elif 'ip_law' in path_str:
            return 'ip_law'
        else:
            return 'miscellaneous'
    
    def get_date_range_folder(self, year):
        """Convert year to date range folder name"""
        if year <= 2018:
            return "2015-2018"
        elif year <= 2020:
            return "2019-2020"
        elif year <= 2022:
            return "2021-2022"
        elif year <= 2024:
            return "2023-2024"
        else:
            return "2025-future"
    
    def analyze_current_structure(self):
        """Analyze current repository structure and collect statistics"""
        print("🔍 Analyzing current repository structure...")
        
        json_files = list(self.source_dir.rglob("*.json"))
        total_files = len(json_files)
        
        print(f"📊 Found {total_files:,} JSON files to process")
        
        # Analyze by date and type
        for file_path in json_files:
            year = self.extract_date_from_file(file_path)
            doc_type = self.get_document_type(file_path)
            date_range = self.get_date_range_folder(year)
            
            self.file_stats[date_range].append({
                'file': file_path,
                'year': year,
                'type': doc_type
            })
            self.date_distribution[date_range] += 1
        
        print("\n📅 Date Distribution Analysis:")
        for date_range, count in sorted(self.date_distribution.items()):
            print(f"  {date_range}: {count:,} files")
        
        return total_files
    
    def create_target_structure(self):
        """Create the new organized directory structure"""
        print(f"\n🏗️ Creating new organized structure at {self.target_dir}")
        
        # Create base directory
        self.target_dir.mkdir(exist_ok=True)
        
        # Create date range directories with subdirectories for document types
        for date_range, files_info in self.file_stats.items():
            date_dir = self.target_dir / date_range
            date_dir.mkdir(exist_ok=True)
            
            # Group by document type within date range
            type_groups = defaultdict(list)
            for file_info in files_info:
                type_groups[file_info['type']].append(file_info)
            
            for doc_type, type_files in type_groups.items():
                type_dir = date_dir / doc_type
                type_dir.mkdir(exist_ok=True)
                
                # If more than max_files_per_dir, create batch subdirectories
                if len(type_files) > self.max_files_per_dir:
                    batches = [type_files[i:i + self.max_files_per_dir] 
                              for i in range(0, len(type_files), self.max_files_per_dir)]
                    
                    for batch_num, batch_files in enumerate(batches, 1):
                        batch_dir = type_dir / f"batch_{batch_num:03d}"
                        batch_dir.mkdir(exist_ok=True)
        
        print("✅ Directory structure created successfully")
    
    def copy_files_to_new_structure(self):
        """Copy files from old structure to new organized structure"""
        print(f"\n📁 Copying files to new structure...")
        
        for date_range, files_info in self.file_stats.items():
            date_dir = self.target_dir / date_range
            
            # Group by document type
            type_groups = defaultdict(list)
            for file_info in files_info:
                type_groups[file_info['type']].append(file_info)
            
            for doc_type, type_files in type_groups.items():
                type_dir = date_dir / doc_type
                
                if len(type_files) <= self.max_files_per_dir:
                    # Copy directly to type directory
                    for file_info in type_files:
                        source_file = file_info['file']
                        target_file = type_dir / source_file.name
                        
                        try:
                            shutil.copy2(source_file, target_file)
                            self.processed_files += 1
                        except Exception as e:
                            print(f"❌ Error copying {source_file}: {e}")
                            self.skipped_files += 1
                else:
                    # Distribute across batch directories
                    batches = [type_files[i:i + self.max_files_per_dir] 
                              for i in range(0, len(type_files), self.max_files_per_dir)]
                    
                    for batch_num, batch_files in enumerate(batches, 1):
                        batch_dir = type_dir / f"batch_{batch_num:03d}"
                        
                        for file_info in batch_files:
                            source_file = file_info['file']
                            target_file = batch_dir / source_file.name
                            
                            try:
                                shutil.copy2(source_file, target_file)
                                self.processed_files += 1
                            except Exception as e:
                                print(f"❌ Error copying {source_file}: {e}")
                                self.skipped_files += 1
                
                if self.processed_files % 1000 == 0:
                    print(f"📈 Progress: {self.processed_files:,} files processed...")
    
    def create_index_files(self):
        """Create index files for the new structure"""
        print(f"\n📋 Creating index files...")
        
        # Main index
        main_index = {
            "repository_info": {
                "name": "Legal Documents Repository (Organized)",
                "description": "Date-based organization with max 999 files per directory",
                "total_files": self.processed_files,
                "organization_date": datetime.now().isoformat(),
                "max_files_per_directory": self.max_files_per_dir
            },
            "date_ranges": {},
            "statistics": dict(self.date_distribution)
        }
        
        # Analyze new structure
        for date_dir in self.target_dir.iterdir():
            if date_dir.is_dir() and date_dir.name != 'indexes':
                date_info = {
                    "total_files": 0,
                    "document_types": {}
                }
                
                for type_dir in date_dir.iterdir():
                    if type_dir.is_dir():
                        file_count = 0
                        batch_info = {}
                        
                        # Count files in type directory
                        direct_files = len(list(type_dir.glob("*.json")))
                        file_count += direct_files
                        
                        # Count files in batch subdirectories
                        for batch_dir in type_dir.iterdir():
                            if batch_dir.is_dir() and batch_dir.name.startswith('batch_'):
                                batch_files = len(list(batch_dir.glob("*.json")))
                                batch_info[batch_dir.name] = batch_files
                                file_count += batch_files
                        
                        type_info = {
                            "file_count": file_count,
                            "direct_files": direct_files,
                            "batches": batch_info if batch_info else None
                        }
                        
                        date_info["document_types"][type_dir.name] = type_info
                        date_info["total_files"] += file_count
                
                main_index["date_ranges"][date_dir.name] = date_info
        
        # Write main index
        index_file = self.target_dir / "repository_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(main_index, f, indent=2, ensure_ascii=False)
        
        # Create README
        readme_content = f"""# Legal Documents Repository (Organized)

## Overview
This repository contains {self.processed_files:,} legal documents organized by date ranges to comply with GitHub's directory display limits (max 999 files per directory).

## Organization Structure
```
legal_documents_repository_organized/
├── 2015-2018/           # Documents from 2015-2018
├── 2019-2020/           # Documents from 2019-2020
├── 2021-2022/           # Documents from 2021-2022
├── 2023-2024/           # Documents from 2023-2024
├── 2025-future/         # Documents from 2025 onwards
└── repository_index.json # Complete index of all documents
```

## Date Range Distribution
"""
        
        for date_range, count in sorted(self.date_distribution.items()):
            readme_content += f"- **{date_range}**: {count:,} documents\n"
        
        readme_content += f"""
## Document Types
Each date range contains subdirectories for different document types:
- `supreme_court/` - Supreme Court decisions
- `circuit_courts/` - Federal Circuit Court decisions
- `district_courts/` - Federal District Court decisions
- `regulations/` - Federal regulations
- `statutes/` - Federal statutes
- `academic/` - Academic papers and law reviews
- `state_courts/` - State court decisions
- `constitutional_law/` - Constitutional law documents
- `contracts/` - Contract-related documents
- `ip_law/` - Intellectual property law documents

## Batch Organization
When a document type within a date range exceeds 999 files, it is organized into batch subdirectories:
- `batch_001/` - Files 1-999
- `batch_002/` - Files 1000-1998
- etc.

## Generated Information
- **Reorganization Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total Files Processed**: {self.processed_files:,}
- **Files Skipped**: {self.skipped_files}
- **Max Files Per Directory**: {self.max_files_per_dir}
"""
        
        readme_file = self.target_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ Index files created successfully")
    
    def validate_organization(self):
        """Validate that no directory exceeds the file limit"""
        print(f"\n✅ Validating organization...")
        
        violations = []
        total_dirs = 0
        total_files_found = 0
        
        for root, dirs, files in os.walk(self.target_dir):
            json_files = [f for f in files if f.endswith('.json')]
            file_count = len(json_files)
            total_files_found += file_count
            total_dirs += 1
            
            if file_count > self.max_files_per_dir:
                violations.append((root, file_count))
        
        if violations:
            print(f"❌ Found {len(violations)} directories exceeding {self.max_files_per_dir} files:")
            for dir_path, count in violations:
                print(f"   {dir_path}: {count} files")
            return False
        else:
            print(f"✅ All directories comply with {self.max_files_per_dir} file limit")
            print(f"📊 Validation Summary:")
            print(f"   - Total directories: {total_dirs}")
            print(f"   - Total files found: {total_files_found:,}")
            print(f"   - Files processed: {self.processed_files:,}")
            print(f"   - Files skipped: {self.skipped_files}")
            return True
    
    def reorganize(self):
        """Main reorganization process"""
        print("🚀 Starting Legal Documents Repository Reorganization")
        print("=" * 60)
        
        # Step 1: Analyze current structure
        total_files = self.analyze_current_structure()
        
        # Step 2: Create new directory structure
        self.create_target_structure()
        
        # Step 3: Copy files to new structure
        self.copy_files_to_new_structure()
        
        # Step 4: Create index files
        self.create_index_files()
        
        # Step 5: Validate organization
        is_valid = self.validate_organization()
        
        print("\n" + "=" * 60)
        print("📋 REORGANIZATION SUMMARY")
        print("=" * 60)
        print(f"✅ Source directory: {self.source_dir}")
        print(f"✅ Target directory: {self.target_dir}")
        print(f"✅ Total files found: {total_files:,}")
        print(f"✅ Files processed: {self.processed_files:,}")
        print(f"❌ Files skipped: {self.skipped_files}")
        print(f"✅ Organization valid: {'Yes' if is_valid else 'No'}")
        print(f"✅ Max files per directory: {self.max_files_per_dir}")
        
        if is_valid:
            print("\n🎉 Repository reorganization completed successfully!")
            print(f"📁 New organized repository available at: {self.target_dir}")
            print("📋 Check repository_index.json for complete file listing")
            print("📖 See README.md for detailed organization information")
        else:
            print("\n⚠️ Repository reorganization completed with validation issues!")
            
        return is_valid

if __name__ == "__main__":
    reorganizer = LegalRepositoryReorganizer()
    success = reorganizer.reorganize()
    exit(0 if success else 1)