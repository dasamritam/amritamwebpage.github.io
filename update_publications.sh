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

# Print start message
log "Starting publication update process..."

# Check if we're in the right directory
if [ ! -f "scholar_sync.py" ]; then
    handle_error "scholar_sync.py not found. Please run this script from the correct directory."
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    log "Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
log "Activating virtual environment..."
source .venv/bin/activate

# Check if virtual environment activation was successful
if [ $? -ne 0 ]; then
    handle_error "Failed to activate virtual environment"
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
log "Running scholar_sync.py..."
python scholar_sync.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    log "Publication update completed successfully!"
    log "Updated file: publications.md"
    log "Backup file: publications.md.backup"
    
    # If using git, commit the changes
    if [ -d ".git" ]; then
        log "Committing changes to git..."
        git add publications.md || log "Warning: Failed to add publications.md to git"
        git commit -m "Update publications [automated]" || log "Warning: Failed to commit changes"
        git push || log "Warning: Failed to push changes"
    fi
    
    log "Backup created at: $BACKUP_DIR/publications_${TIMESTAMP}.md"
else
    handle_error "Publication update failed"
fi

# Deactivate virtual environment
deactivate

log "Process completed!" 