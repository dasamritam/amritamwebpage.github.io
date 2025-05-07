#!/bin/bash

# Exit on error
set -e

# Create timestamp for backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="publication_backups"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to handle errors
handle_error() {
    log "ERROR: $1"
    exit 1
}

# Start message
echo "Starting publication update process..."

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if virtual environment activation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Install/update requirements
log "Installing/updating requirements..."
pip install -r requirements.txt || handle_error "Failed to install requirements"

# Backup current publications file if it exists
if [ -f "publications.md" ]; then
    log "Creating backup of current publications file..."
    cp "publications.md" "$BACKUP_DIR/publications_${TIMESTAMP}.md" || handle_error "Failed to create backup"
fi

# Run the Python script
echo "Running scholar_sync.py..."
python scholar_sync.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "Publication update completed successfully!"
    echo "Updated file: publications.md"
    echo "Backup file: publications.md.backup"
    
    # Add and commit changes to git
    echo "Committing changes to git..."
    git add publications.md
    git commit -m "Update publications [automated]"
    git push
    
    log "Backup created at: $BACKUP_DIR/publications_${TIMESTAMP}.md"
else
    echo "Error: Publication update failed"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo "Process completed!" 