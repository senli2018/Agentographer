#!/bin/bash

# Set application directory and log files
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$APP_DIR/logs/app.log"
ERROR_LOG="$APP_DIR/logs/error.log"
DEFAULT_LINES=50

# Display help information
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help information"
    echo "  -e, --error    View error logs"
    echo "  -f, --follow   Continuously view log updates"
    echo "  -n, --lines N  Show last N lines (default: $DEFAULT_LINES)"
    echo ""
    echo "Examples:"
    echo "  $0             Show last $DEFAULT_LINES lines of application logs"
    echo "  $0 -e          Show last $DEFAULT_LINES lines of error logs"
    echo "  $0 -f          Continuously view application log updates"
    echo "  $0 -e -f       Continuously view error log updates"
    echo "  $0 -n 100      Show last 100 lines of application logs"
}

# Initialize variables
SHOW_ERROR=false
FOLLOW=false
LINES=$DEFAULT_LINES

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -e|--error)
            SHOW_ERROR=true
            shift
            ;;
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -n|--lines)
            if [[ $# -lt 2 ]] || ! [[ $2 =~ ^[0-9]+$ ]]; then
                echo "Error: -n option requires a numeric argument"
                exit 1
            fi
            LINES=$2
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Determine which log file to view
if [ "$SHOW_ERROR" = true ]; then
    CURRENT_LOG=$ERROR_LOG
    LOG_TYPE="error logs"
else
    CURRENT_LOG=$LOG_FILE
    LOG_TYPE="application logs"
fi

# Check if log file exists
if [ ! -f "$CURRENT_LOG" ]; then
    echo "Error: $LOG_TYPE file does not exist: $CURRENT_LOG"
    exit 1
fi

# Display logs
if [ "$FOLLOW" = true ]; then
    echo "Displaying real-time updates of $LOG_TYPE (press Ctrl+C to exit)..."
    tail -n "$LINES" -f "$CURRENT_LOG"
else
    echo "Displaying last $LINES lines of $LOG_TYPE:"
    tail -n "$LINES" "$CURRENT_LOG"
fi 