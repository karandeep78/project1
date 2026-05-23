#!/bin/bash

# Phishing Detector Setup Script
# This script sets up the environment with all dependencies and fixes

echo "========================================="
echo "Phishing Detector - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application, use:"
echo "  python app.py"
echo ""
echo "The application will run on http://localhost:5001"
echo ""
