"""
Monitor the comprehensive repository expansion progress
"""

import time
import json
from pathlib import Path
from collections import defaultdict
import os

def monitor_expansion_progress():
    """Monitor the repository expansion progress in real-time"""
    
    repo_path = Path("/app/legal_documents_repository_organized")
    
    print("📊 REPOSITORY EXPANSION PROGRESS MONITOR")
    print("=" * 80)
    
    # Initial count
    initial_count = count_documents(repo_path)
    print(f"📁 Initial document count: {initial_count:,}")
    print("🎯 Target: 100,000+ documents")
    print("=" * 80)
    
    start_time = time.time()
    last_count = initial_count
    
    while True:
        try:
            current_count = count_documents(repo_path)
            elapsed_time = time.time() - start_time
            
            # Calculate progress
            documents_added = current_count - initial_count
            target_remaining = max(0, 100000 - current_count)
            progress_percentage = (current_count / 100000) * 100
            
            # Calculate rate
            if elapsed_time > 0:
                docs_per_hour = documents_added / (elapsed_time / 3600)
                if docs_per_hour > 0:
                    eta_hours = target_remaining / docs_per_hour
                else:
                    eta_hours = float('inf')
            else:
                docs_per_hour = 0
                eta_hours = float('inf')
            
            # Clear screen and show current status
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print("📊 REPOSITORY EXPANSION PROGRESS MONITOR")
            print("=" * 80)
            print(f"📁 Current document count: {current_count:,}")
            print(f"📈 Documents added this session: {documents_added:,}")
            print(f"🎯 Progress to 100,000: {progress_percentage:.1f}%")
            print(f"🔄 Documents remaining: {target_remaining:,}")
            print(f"⏱️  Runtime: {elapsed_time/3600:.1f} hours")
            print(f"🚀 Rate: {docs_per_hour:.0f} docs/hour")
            
            if eta_hours != float('inf') and eta_hours > 0:
                print(f"🕐 ETA to completion: {eta_hours:.1f} hours")
            else:
                print("🕐 ETA: Calculating...")
            
            # Show directory breakdown
            print("\n📂 Directory Breakdown:")
            directory_stats = analyze_directories(repo_path)
            for date_range, count in directory_stats.items():
                print(f"  • {date_range}: {count:,} documents")
            
            # Progress bar
            print(f"\n{'█' * int(progress_percentage // 2)}{'░' * (50 - int(progress_percentage // 2))} {progress_percentage:.1f}%")
            
            # Check for completion
            if current_count >= 100000:
                print("\n🎉 TARGET ACHIEVED! Repository has reached 100,000+ documents!")
                break
            
            # Check if expansion stopped
            if current_count == last_count and elapsed_time > 300:  # No change for 5 minutes
                print("\n⚠️  Expansion appears to have stopped. Check expansion processes.")
            
            last_count = current_count
            
            print(f"\n⏰ Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Press Ctrl+C to stop monitoring...")
            
            time.sleep(30)  # Update every 30 seconds
            
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Error monitoring: {e}")
            time.sleep(10)

def count_documents(repo_path):
    """Count total documents in repository"""
    if not repo_path.exists():
        return 0
    return len(list(repo_path.rglob("*.json")))

def analyze_directories(repo_path):
    """Analyze document distribution by directory"""
    directory_stats = defaultdict(int)
    
    try:
        for date_dir in repo_path.iterdir():
            if date_dir.is_dir() and not date_dir.name.startswith('.'):
                count = len(list(date_dir.rglob("*.json")))
                directory_stats[date_dir.name] = count
    except Exception as e:
        print(f"Error analyzing directories: {e}")
    
    # Sort by directory name
    return dict(sorted(directory_stats.items()))

def show_detailed_analysis():
    """Show detailed repository analysis"""
    repo_path = Path("/app/legal_documents_repository_organized")
    
    print("\n📊 DETAILED REPOSITORY ANALYSIS")
    print("=" * 80)
    
    try:
        # Overall stats
        total_docs = count_documents(repo_path)
        print(f"📁 Total Documents: {total_docs:,}")
        
        # Directory analysis
        for date_dir in sorted(repo_path.iterdir()):
            if date_dir.is_dir() and not date_dir.name.startswith('.'):
                print(f"\n📂 {date_dir.name}:")
                
                # Subdirectory analysis
                subdirs = defaultdict(int)
                for subdir in date_dir.iterdir():
                    if subdir.is_dir():
                        count = len(list(subdir.rglob("*.json")))
                        subdirs[subdir.name] = count
                
                for subdir, count in sorted(subdirs.items()):
                    print(f"  • {subdir}: {count:,} documents")
                    
                    # Check for batch organization
                    subdir_path = date_dir / subdir
                    if subdir_path.exists():
                        batches = [d for d in subdir_path.iterdir() if d.is_dir() and d.name.startswith('batch_')]
                        if batches:
                            print(f"    └─ Organized in {len(batches)} batches")
        
        # Check for reports
        report_files = list(repo_path.glob("*report*.json"))
        if report_files:
            print(f"\n📄 Report Files Found: {len(report_files)}")
            for report in report_files:
                print(f"  • {report.name}")
                
    except Exception as e:
        print(f"❌ Error in detailed analysis: {e}")

if __name__ == "__main__":
    try:
        # Show initial analysis
        show_detailed_analysis()
        
        print("\nStarting real-time monitoring...")
        time.sleep(3)
        
        # Start monitoring
        monitor_expansion_progress()
        
    except Exception as e:
        print(f"❌ Monitor error: {e}")
    
    print("\n👋 Monitoring session ended")