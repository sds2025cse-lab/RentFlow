#!/bin/bash
# RentFlow Quick Start Script

echo "================================"
echo "RentFlow E-Commerce Quick Start"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed"

# Copy environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Stripe keys if needed."
fi

# Create database
echo ""
echo "Initializing database..."
python run.py &
FLASK_PID=$!
sleep 3
kill $FLASK_PID 2>/dev/null
echo "✅ Database initialized"

# Run the application
echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Starting RentFlow..."
echo ""
echo "The application will run on: http://localhost:5000"
echo ""
echo "Test Credentials:"
echo "  Admin Email: admin@rentflow.com"
echo "  Password: admin123"
echo ""
echo "Stripe Test Card: 4242 4242 4242 4242"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
