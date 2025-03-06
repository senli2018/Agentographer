#!/bin/bash

# Set application name and directory
APP_NAME="FastAPI App"
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$APP_DIR/app.pid"

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "PID file does not exist, application may not be running"
    exit 0
fi

# Read PID
PID=$(cat "$PID_FILE")

# Check if process exists
if ! ps -p "$PID" > /dev/null; then
    echo "Process $PID does not exist, may have already stopped"
    rm "$PID_FILE"
    exit 0
fi

# Try to stop the process normally
echo "Stopping $APP_NAME (PID: $PID)..."
kill "$PID"

# Wait for process to end
TIMEOUT=30
COUNT=0
while ps -p "$PID" > /dev/null && [ $COUNT -lt $TIMEOUT ]; do
    echo "Waiting for process to end... ($COUNT/$TIMEOUT)"
    sleep 1
    COUNT=$((COUNT + 1))
done

# Check if process has ended
if ps -p "$PID" > /dev/null; then
    echo "Process did not end within $TIMEOUT seconds, attempting to force terminate..."
    kill -9 "$PID"
    sleep 2
fi

# Final check
if ps -p "$PID" > /dev/null; then
    echo "Unable to terminate process $PID"
    exit 1
else
    echo "$APP_NAME has been stopped"
    rm "$PID_FILE"
fi 