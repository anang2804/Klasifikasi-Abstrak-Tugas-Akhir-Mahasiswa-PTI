"""
Utility functions untuk aplikasi
"""
import os
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_uploaded_file(file) -> str:
    """
    Save uploaded file and return filepath
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)
        
        return filepath
    
    return None


def extract_text_from_txt(filepath: str) -> str:
    """
    Extract text from TXT file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""


def format_confidence(confidence: float) -> str:
    """
    Format confidence score untuk display
    """
    percentage = confidence * 100
    
    if percentage >= 80:
        return f"{percentage:.2f}% (Tinggi)"
    elif percentage >= 60:
        return f"{percentage:.2f}% (Sedang)"
    else:
        return f"{percentage:.2f}% (Rendah)"


def get_label_color(label: str) -> str:
    """
    Get Bootstrap color class for label
    """
    colors = {
        'RPL': 'primary',
        'TKJ': 'success'
    }
    return colors.get(label, 'secondary')


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text dengan ellipsis
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'
