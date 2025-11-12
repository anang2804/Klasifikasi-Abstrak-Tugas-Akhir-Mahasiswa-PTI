"""
Database models untuk aplikasi
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Abstract(db.Model):
    """Model untuk menyimpan data abstrak tugas akhir"""
    __tablename__ = 'abstracts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    abstract_text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(500))
    
    # Label: RPL atau TKJ
    label = db.Column(db.String(10))  # 'RPL' atau 'TKJ'
    predicted_label = db.Column(db.String(10))  # Hasil prediksi
    confidence = db.Column(db.Float)  # Confidence score
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_training_data = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Abstract {self.title[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'abstract_text': self.abstract_text,
            'url': self.url,
            'label': self.label,
            'predicted_label': self.predicted_label,
            'confidence': self.confidence,
            'is_training_data': self.is_training_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ModelMetrics(db.Model):
    """Model untuk menyimpan metrik evaluasi model"""
    __tablename__ = 'model_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), default='KNN')
    k_value = db.Column(db.Integer)
    
    # Metrics
    accuracy = db.Column(db.Float)
    precision_rpl = db.Column(db.Float)
    precision_tkj = db.Column(db.Float)
    recall_rpl = db.Column(db.Float)
    recall_tkj = db.Column(db.Float)
    f1_rpl = db.Column(db.Float)
    f1_tkj = db.Column(db.Float)
    
    # Training info
    training_samples = db.Column(db.Integer)
    test_samples = db.Column(db.Integer)
    trained_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ModelMetrics {self.model_name} k={self.k_value} acc={self.accuracy:.2f}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_name': self.model_name,
            'k_value': self.k_value,
            'accuracy': self.accuracy,
            'precision': {
                'RPL': self.precision_rpl,
                'TKJ': self.precision_tkj
            },
            'recall': {
                'RPL': self.recall_rpl,
                'TKJ': self.recall_tkj
            },
            'f1_score': {
                'RPL': self.f1_rpl,
                'TKJ': self.f1_tkj
            },
            'training_samples': self.training_samples,
            'test_samples': self.test_samples,
            'trained_at': self.trained_at.isoformat() if self.trained_at else None
        }


class ClassificationHistory(db.Model):
    """Model untuk menyimpan history klasifikasi (Data Uji)"""
    __tablename__ = 'classification_history'
    
    id = db.Column(db.Integer, primary_key=True)
    abstract_text = db.Column(db.Text, nullable=False)
    predicted_label = db.Column(db.String(10), nullable=False)  # RPL atau TKJ
    confidence = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(20), default='manual')  # 'manual', 'upload', 'batch'
    classified_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ClassificationHistory {self.predicted_label} conf={self.confidence:.2f}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'abstract_text': self.abstract_text[:100] + '...' if len(self.abstract_text) > 100 else self.abstract_text,
            'predicted_label': self.predicted_label,
            'confidence': self.confidence,
            'source': self.source,
            'classified_at': self.classified_at.isoformat() if self.classified_at else None
        }
