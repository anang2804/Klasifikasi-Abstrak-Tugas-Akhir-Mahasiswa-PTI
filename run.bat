@echo off
REM Script untuk menjalankan aplikasi di Windows

echo ===================================
echo Klasifikasi Abstrak Tugas Akhir PTI
echo ===================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
python init_db.py

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True)"

REM Run application
echo.
echo Starting Flask application...
echo Access the application at: http://localhost:5000
echo.
python app.py

pause
