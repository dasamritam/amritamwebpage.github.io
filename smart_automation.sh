#!/bin/bash

# Smart automation that handles sleep scenarios
# Runs every Sunday at 23:25 CEST, or when laptop wakes up after missing it

LOG_FILE="/Users/amdas/Library/CloudStorage/OneDrive-TUEindhoven/amritamwebpage.github.io/update_log.txt"
SCRIPT_DIR="/Users/amdas/Library/CloudStorage/OneDrive-TUEindhoven/amritamwebpage.github.io"

# Function to check if we should run the update
should_run_update() {
    local current_day=$(date '+%u')  # 1=Monday, 7=Sunday
    local current_time=$(date '+%H:%M')
    local current_date=$(date '+%Y-%m-%d')
    
    # Check if it's Sunday and time is 23:46 (test time)
    if [ "$current_day" = "7" ] && [ "$current_time" = "23:46" ]; then
        return 0  # Should run
    fi
    
    # Check if we missed the update (Sunday after 23:46 but before midnight)
    if [ "$current_day" = "7" ] && [ "$current_time" \> "23:46" ] && [ "$current_time" \< "23:59" ]; then
        # Check if we already ran today
        if ! grep -q "Scheduled update completed.*$current_date" "$LOG_FILE"; then
            return 0  # Should run (missed it)
        fi
    fi
    
    return 1  # Should not run
}

# Main execution
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Smart automation check..." >> "$LOG_FILE"

if should_run_update; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running publication update..." >> "$LOG_FILE"
    cd "$SCRIPT_DIR"
    ./update_publications.sh
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Update completed." >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No update needed at this time." >> "$LOG_FILE"
fi 