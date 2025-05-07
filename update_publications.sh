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

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    log "Activating virtual environment..."
    source .venv/bin/activate || handle_error "Failed to activate virtual environment"
fi

# Install/update requirements
log "Installing/updating requirements..."
pip install -r requirements.txt || handle_error "Failed to install requirements"

# Backup current publications file if it exists
if [ -f "publications.md" ]; then
    log "Creating backup of current publications file..."
    cp "publications.md" "$BACKUP_DIR/publications_${TIMESTAMP}.md" || handle_error "Failed to create backup"
fi

# Run the publication update script
log "Starting publication update..."
python scholar_sync.py || handle_error "Failed to update publications"

# Check if new file was created
if [ ! -f "publications_new.md" ]; then
    handle_error "New publications file was not created"
fi

# Verify the new file has content
if [ ! -s "publications_new.md" ]; then
    handle_error "New publications file is empty"
fi

# If the script was successful, update the main publications file
if [ $? -eq 0 ]; then
    # Move the new file to replace the current one
    log "Replacing old publications file with new one..."
    mv "publications_new.md" "publications.md" || handle_error "Failed to replace publications file"
    
    # If using git, commit the changes
    if [ -d ".git" ]; then
        log "Committing changes to git..."
        git add publications.md
        git commit -m "Update publications [automated]"
        git push
    fi
    
    log "Publication update completed successfully!"
    log "Backup created at: $BACKUP_DIR/publications_${TIMESTAMP}.md"
else
    echo "Error updating publications. Check the logs for details."
    exit 1
fi

# Deactivate virtual environment
if [ -d ".venv" ]; then
    deactivate
fi 