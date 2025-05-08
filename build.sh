#!/bin/bash

# Install dependencies
pip install -r requirements-vercel.txt

# Create SQLite database directory if it doesn't exist
mkdir -p .vercel/output/static/

# Print environment information
echo "Python version:"
python --version

# Print installed packages
pip list

echo "Build script completed successfully"