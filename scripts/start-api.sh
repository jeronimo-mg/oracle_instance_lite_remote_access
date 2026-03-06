#!/bin/bash
# Start the LiteMode Management API

# Get current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_ROOT="$(dirname "$DIR")"

cd "$PROJECT_ROOT"

# Optional: define DB path
export DB_PATH="$PROJECT_ROOT/litemode.db"

# Ensure DASHBOARD_PASSWORD is exported if defined in current shell
if [ ! -z "$DASHBOARD_PASSWORD" ]; then
    export DASHBOARD_PASSWORD="$DASHBOARD_PASSWORD"
    echo "Using custom dashboard password detected in environment."
else
    echo "Warning: DASHBOARD_PASSWORD not found in environment, using default."
fi

# Start the API using python3
python3 src/api/main.py
