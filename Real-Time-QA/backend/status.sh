#!/bin/bash

# Set application name and directory
APP_NAME="FastAPI App"
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$APP_DIR/app.pid"
LOG_FILE="$APP_DIR/logs/app.log"
ERROR_LOG="$APP_DIR/logs/error.log"

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "Status: Not running (PID file does not exist)"
    exit 0
fi

# Read PID
PID=$(cat "$PID_FILE")

# Check if process exists
if ! ps -p "$PID" > /dev/null; then
    echo "Status: Not running (PID: $PID does not exist)"
    echo "Deleting expired PID file"
    rm "$PID_FILE"
    exit 0
fi

# Get process information
PROCESS_INFO=$(ps -p "$PID" -o pid,ppid,user,%cpu,%mem,vsz,rss,stat,start,time,command | tail -n 1)
UPTIME=$(ps -p "$PID" -o etime= | tr -d ' ')

# Display status information
echo "Status: Running"
echo "PID: $PID"
echo "Process info: $PROCESS_INFO"
echo "Uptime: $UPTIME"

# Display recent logs
echo ""
echo "Recent application logs (last 5 lines):"
if [ -f "$LOG_FILE" ]; then
    tail -n 5 "$LOG_FILE"
else
    echo "Log file does not exist: $LOG_FILE"
fi

echo ""
echo "Recent error logs (last 5 lines):"
if [ -f "$ERROR_LOG" ]; then
    tail -n 5 "$ERROR_LOG"
else
    echo "Error log file does not exist: $ERROR_LOG"
fi

echo ""
echo "Use ./logs.sh to view complete logs" 