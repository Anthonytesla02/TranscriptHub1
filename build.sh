#!/bin/bash

echo "Starting TranscriptHub build process for Vercel deployment..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements-vercel.txt

# Create necessary directories
echo "Creating required directories..."
mkdir -p .vercel/output/static/

# Ensure SQLite directory exists (for Vercel serverless environment)
SQLITE_DIR="$(dirname "transcripthub.db")"
if [ ! -z "$SQLITE_DIR" ] && [ "$SQLITE_DIR" != "." ]; then
    mkdir -p "$SQLITE_DIR"
    echo "Created SQLite database directory: $SQLITE_DIR"
fi

# Check for Mistral API key in environment variables
if [ -z "$MISTRAL_API_KEY" ]; then
    echo "WARNING: MISTRAL_API_KEY environment variable is not set."
    echo "You should set this in your Vercel project settings."
    echo "API calls to Mistral AI will fail without a valid API key."
fi

# Print environment information for debugging
echo "Python version:"
python --version

echo "Installed packages:"
pip list

echo "Build script completed successfully"