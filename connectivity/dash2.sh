#!/bin/bash

# Configuration
HOST="192.168.0.169"
RETRY_INTERVAL_UNREACHABLE=10 # Interval in seconds when unreachable
RETRY_INTERVAL_REACHABLE=60  # Interval in seconds when reachable
USERNAME="rover2"
PASSWORD="rover2"

# Colors
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
RESET=$(tput sgr0)

# Clear the terminal and set up the dashboard
setup_dashboard() {
    clear
    echo "========================================"
    echo "           Host Status Dashboard        "
    echo "========================================"
    echo "Host: $HOST"
    echo "----------------------------------------"
    echo "Status:         "
    echo "Last Checked:   "
    echo "Next Check In:  "
    echo "========================================"
}

# Update the dashboard
update_dashboard() {
    local status="$1"
    local color="$2"
    local next_check="$3"

    # Status
    tput cup 5 16  # Move to "Status:" value position
    echo -n "                    "  # Clear the line
    echo -n "${color}${status}${RESET}"

    # Last Checked
    tput cup 6 16  # Move to "Last Checked:" value position
    echo -n "                    "  # Clear the line
    echo -n "$(date '+%Y-%m-%d %H:%M:%S')"

    # Next Check In
    tput cup 7 16  # Move to "Next Check In:" value position
    echo -n "                    "  # Clear the line
    echo -n "${next_check}s"
}

# Function to check host reachability via ping
check_ping() {
    ping -c 1 -W 1 "$HOST" > /dev/null 2>&1
    return $? # 0 if reachable, 1 if not
}

# Function to check SSH reachability
check_ssh() {
    sshpass -p "$PASSWORD" ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$USERNAME@$HOST" exit > /dev/null 2>&1
    return $? # 0 if reachable, 1 if not
}

# Main loop
main() {
    setup_dashboard

    while true; do
        # Check host reachability
        if check_ping; then
            if check_ssh; then
                update_dashboard "🟢 Reachable via SSH" "$GREEN" "$RETRY_INTERVAL_REACHABLE"
                sleep "$RETRY_INTERVAL_REACHABLE"
                continue
            else
                update_dashboard "🔴 SSH Unreachable" "$RED" "$RETRY_INTERVAL_UNREACHABLE"
            fi
        else
            update_dashboard "🔴 Host Unreachable" "$RED" "$RETRY_INTERVAL_UNREACHABLE"
        fi
        
        # Wait before retrying
        sleep "$RETRY_INTERVAL_UNREACHABLE"
    done
}

# Run the script
main
