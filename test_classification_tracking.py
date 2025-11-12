"""
Script untuk testing tracking data uji
"""
from app import app, db
from models import ClassificationHistory, Abstract

def test_tracking():
    with app.app_context():
        # Tampilkan statistik
        training_count = Abstract.query.filter(Abstract.label.isnot(None)).count()
        test_count = ClassificationHistory.query.count()
        
        print("\n=== STATISTIK DATA ===")
        print(f"Data Latih: {training_count}")
        print(f"Data Uji: {test_count}")
        
        if test_count > 0:
            print("\n=== DETAIL DATA UJI ===")
            histories = ClassificationHistory.query.order_by(ClassificationHistory.classified_at.desc()).limit(5).all()
            for i, h in enumerate(histories, 1):
                print(f"\n{i}. Prediksi: {h.predicted_label} (Confidence: {h.confidence:.2%})")
                print(f"   Source: {h.source}")
                print(f"   Waktu: {h.classified_at}")
                print(f"   Text: {h.abstract_text[:100]}...")
        else:
            print("\nBelum ada data uji. Silakan coba klasifikasi melalui menu Klasifikasi.")

if __name__ == '__main__':
    test_tracking()
