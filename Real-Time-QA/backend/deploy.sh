#!/bin/bash

# Set application name and directory
APP_NAME="FastAPI App"
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$APP_DIR/app.pid"
LOG_FILE="$APP_DIR/logs/app.log"
ERROR_LOG="$APP_DIR/logs/error.log"

# Ensure log directory exists
mkdir -p "$APP_DIR/logs"

# Check if application is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo "Application is already running, PID: $PID"
        exit 1
    else
        echo "Found expired PID file, will delete"
        rm "$PID_FILE"
    fi
fi

# Start the application
echo "Starting $APP_NAME..."
cd "$APP_DIR" || exit 1

# Use nohup to run the application in the background
nohup python run.py > "$LOG_FILE" 2> "$ERROR_LOG" &

# Save PID
echo $! > "$PID_FILE"
echo "$APP_NAME has started, PID: $!"
echo "Log file: $LOG_FILE"
echo "Error log: $ERROR_LOG"

# Wait a few seconds to check if the application started successfully
sleep 3
if ps -p "$(cat "$PID_FILE")" > /dev/null; then
    echo "Application started successfully!"
    echo "Use ./status.sh to check status, use ./logs.sh to view logs"
else
    echo "Application failed to start, please check error log: $ERROR_LOG"
    exit 1
fi 