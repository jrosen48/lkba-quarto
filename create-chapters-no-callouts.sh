#!/bin/bash

# This script creates DOCX chapters WITHOUT callouts for publisher delivery

echo "=========================================="
echo "Creating DOCX Chapters WITHOUT Callouts"
echo "=========================================="
echo ""

# Step 1: Create backup of trail files
echo "Step 1: Creating backup of trail files..."
mkdir -p trail_backups_nocallouts
cp Trail_*.qmd trail_backups_nocallouts/
echo "  ✓ Backup created in trail_backups_nocallouts/"
echo ""

# Step 2: Remove callouts from all trail files
echo "Step 2: Removing callouts from trail files..."
python3 remove-callouts-for-docx.py
echo ""

# Step 3: Run the standard chapter creation script
echo "Step 3: Rendering DOCX files..."
./create-chapters.sh
echo ""

# Step 4: Restore original files
echo "Step 4: Restoring original trail files..."
cp trail_backups_nocallouts/*.qmd .
echo "  ✓ Original files restored"
echo ""

echo "=========================================="
echo "DONE! DOCX files (without callouts) are in docx_chapters/"
echo "=========================================="
