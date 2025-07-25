#!/bin/bash

# Get the absolute path to the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create the cron job entry
CRON_JOB="0 2 * * 0 cd $SCRIPT_DIR && ./update_publications.sh >> update_log.txt 2>&1"

echo "Setting up cron job for automatic publication updates..."
echo "Cron job will run every Sunday at 2 AM"
echo ""

# Remove any existing cron jobs for this script
echo "Removing any existing cron jobs..."
(crontab -l 2>/dev/null | grep -v "update_publications.sh") | crontab -

# Add the new cron job
echo "Adding new cron job..."
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# Verify the cron job was added
echo "Verifying cron job installation..."
crontab -l | grep "update_publications.sh"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Cron job successfully installed!"
    echo "The publication update will run automatically every Sunday at 2 AM"
    echo "Logs will be saved to update_log.txt"
else
    echo ""
    echo "❌ Failed to install cron job"
    exit 1
fi 