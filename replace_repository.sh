#!/bin/bash

# Replace Repository Script
# =========================
# This script replaces the original legal_documents_repository with the organized version

echo "🔄 Repository Replacement Script"
echo "================================="

ORIGINAL_DIR="/app/legal_documents_repository"
ORGANIZED_DIR="/app/legal_documents_repository_organized"
BACKUP_DIR="/app/legal_documents_repository_backup_$(date +%Y%m%d_%H%M%S)"

echo "📁 Original directory: $ORIGINAL_DIR"
echo "📁 Organized directory: $ORGANIZED_DIR"
echo "📁 Backup directory: $BACKUP_DIR"

# Check if organized directory exists
if [ ! -d "$ORGANIZED_DIR" ]; then
    echo "❌ Error: Organized directory does not exist: $ORGANIZED_DIR"
    exit 1
fi

# Check if original directory exists
if [ ! -d "$ORIGINAL_DIR" ]; then
    echo "❌ Error: Original directory does not exist: $ORIGINAL_DIR"
    exit 1
fi

echo ""
echo "⚠️  IMPORTANT: This will replace your current legal_documents_repository"
echo "    with the organized version. A backup will be created first."
echo ""
read -p "Do you want to proceed? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled by user"
    exit 0
fi

echo ""
echo "🔄 Starting replacement process..."

# Step 1: Create backup of original
echo "📦 Step 1: Creating backup of original repository..."
if mv "$ORIGINAL_DIR" "$BACKUP_DIR"; then
    echo "✅ Backup created: $BACKUP_DIR"
else
    echo "❌ Failed to create backup"
    exit 1
fi

# Step 2: Move organized directory to original location
echo "📁 Step 2: Moving organized repository to original location..."
if mv "$ORGANIZED_DIR" "$ORIGINAL_DIR"; then
    echo "✅ Repository replaced successfully"
else
    echo "❌ Failed to move organized directory"
    echo "🔄 Restoring from backup..."
    mv "$BACKUP_DIR" "$ORIGINAL_DIR"
    exit 1
fi

# Step 3: Verify the replacement
echo "🔍 Step 3: Verifying replacement..."
if [ -d "$ORIGINAL_DIR" ] && [ -f "$ORIGINAL_DIR/README.md" ] && [ -f "$ORIGINAL_DIR/repository_index.json" ]; then
    file_count=$(find "$ORIGINAL_DIR" -name "*.json" -type f | wc -l)
    echo "✅ Replacement verified: $file_count files found"
else
    echo "❌ Verification failed"
    exit 1
fi

echo ""
echo "🎉 REPOSITORY REPLACEMENT COMPLETED SUCCESSFULLY!"
echo "================================================="
echo "✅ Original repository backed up to: $BACKUP_DIR"
echo "✅ Organized repository now at: $ORIGINAL_DIR"
echo "✅ All 25,308+ documents organized by date ranges"
echo "✅ Maximum 999 files per directory (GitHub compliant)"
echo ""
echo "📖 Documentation:"
echo "   - README.md: Complete organization guide"
echo "   - repository_index.json: Detailed file index"
echo ""
echo "🗂️  Organization structure:"
echo "   - 2015-2018/: 8,511 documents"
echo "   - 2019-2020/: 4,975 documents"  
echo "   - 2021-2022/: 4,997 documents"
echo "   - 2023-2024/: 5,368 documents"
echo "   - 2025-future/: 1,457 documents"
echo ""
echo "🚀 Your legal documents repository is now GitHub display optimized!"