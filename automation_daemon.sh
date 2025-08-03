#!/bin/bash

# Automation daemon for publication updates
# Runs every Sunday at 23:25 CEST

LOG_FILE="/Users/amdas/Library/CloudStorage/OneDrive-TUEindhoven/amritamwebpage.github.io/update_log.txt"
SCRIPT_DIR="/Users/amdas/Library/CloudStorage/OneDrive-TUEindhoven/amritamwebpage.github.io"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting automation daemon..." >> "$LOG_FILE"

while true; do
    # Get current time in CEST
    CURRENT_TIME=$(date '+%H:%M')
    CURRENT_DAY=$(date '+%u')  # 1=Monday, 7=Sunday
    
    # Check if it's Sunday (day 7) and time is 23:25
    if [ "$CURRENT_DAY" = "7" ] && [ "$CURRENT_TIME" = "23:25" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running scheduled publication update..." >> "$LOG_FILE"
        cd "$SCRIPT_DIR"
        ./update_publications.sh
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Scheduled update completed." >> "$LOG_FILE"
        
        # Sleep for 2 minutes to avoid running multiple times
        sleep 120
    else
        # Sleep for 1 minute before checking again
        sleep 60
    fi
done 