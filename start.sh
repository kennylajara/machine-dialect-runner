#!/bin/bash

# Machine Dialect Runner startup script

set -e

echo "🚀 Starting Machine Dialect Runner..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Install dependencies if requirements.txt exists and is newer than a flag file
if [ -f requirements.txt ]; then
    if [ ! -f .deps_installed ] || [ requirements.txt -nt .deps_installed ]; then
        echo "📦 Installing dependencies..."
        if command -v pip3 &> /dev/null; then
            pip3 install -r requirements.txt
        else
            pip install -r requirements.txt
        fi
        touch .deps_installed
        echo "✅ Dependencies installed successfully"
    else
        echo "✅ Dependencies are up to date"
    fi
fi

# Set default port if not specified
PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

echo "🌐 Starting server on http://$HOST:$PORT"
echo "📚 Documentation will be available at http://$HOST:$PORT/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 main.py