#!/bin/bash

# Script untuk menjalankan aplikasi

echo "==================================="
echo "Klasifikasi Abstrak Tugas Akhir PTI"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv venv
    echo "Virtual environment created!"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python init_db.py

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True)"

# Run application
echo ""
echo "Starting Flask application..."
echo "Access the application at: http://localhost:5000"
echo ""
python app.py
