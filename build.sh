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

# Create directory for static files if it doesn't exist
mkdir -p static

# Display Python and package versions for debugging
echo "Python version:"
python --version
echo "Installed packages:"
pip list

echo "Build completed successfully!"