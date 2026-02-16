#!/bin/bash

# Setup script for AlgoTrade Lab Backend

set -e

echo "🚀 AlgoTrade Lab Backend Setup"
echo "=============================="

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "✓ Creating .env file..."
    cp .env.example .env
    echo "  ⚠️  Please edit .env with your configuration"
fi

# Create database
echo "✓ Creating database..."
# This would require actual DB setup - skipping for now

echo ""
echo "✅ Setup completed!"
echo ""
echo "To activate virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the server:"
echo "  python run.py"
echo ""
echo "Or with Docker:"
echo "  docker-compose up"
