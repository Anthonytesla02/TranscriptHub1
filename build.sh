#!/bin/bash
# build.sh - Setup script for Vercel deployment

echo "Running build script for Vercel deployment..."

# Make sure pip is updated
pip install --upgrade pip

# Install Python dependencies from Vercel-specific requirements file
if [ -f "requirements-vercel.txt" ]; then
  echo "Installing from requirements-vercel.txt..."
  pip install -r requirements-vercel.txt
else
  echo "Installing from requirements.txt..."
  pip install -r requirements.txt
fi

# Create sqlite database directory if it doesn't exist
mkdir -p .vercel/storage

echo "Build completed successfully!"