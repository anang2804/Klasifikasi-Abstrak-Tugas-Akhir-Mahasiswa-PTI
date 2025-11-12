"""
Configuration settings untuk aplikasi
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    
    # KNN Model Settings
    KNN_K_VALUE = 5
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Scraping Settings
    BASE_URL = 'https://ejournal.unesa.ac.id/index.php/it-edu'
    START_YEAR = 2024
    END_YEAR = 2024
