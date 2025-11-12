"""
Script untuk training model KNN
"""
from app import app
from classifier import KNNClassifier
from models import Abstract
import os

def train_model():
    with app.app_context():
        print("=" * 70)
        print("TRAINING MODEL KNN")
        print("=" * 70)
        
        # Ambil data berlabel
        labeled_data = Abstract.query.filter(Abstract.label.isnot(None)).all()
        
        print(f"\n📊 DATA TRAINING:")
        print(f"   Total data berlabel: {len(labeled_data)}")
        
        if len(labeled_data) < 10:
            print(f"\n⚠️  PERINGATAN: Data terlalu sedikit!")
            print(f"   Minimal 10 data berlabel diperlukan untuk training yang baik.")
            print(f"   Saat ini hanya ada {len(labeled_data)} data.")
            print(f"\n   Training tetap dilanjutkan untuk testing...")
        
        # Hitung distribusi label
        rpl_count = sum(1 for d in labeled_data if d.label == 'RPL')
        tkj_count = sum(1 for d in labeled_data if d.label == 'TKJ')
        
        print(f"   - RPL: {rpl_count}")
        print(f"   - TKJ: {tkj_count}")
        
        # Prepare data
        texts = [d.abstract_text for d in labeled_data]
        labels = [d.label for d in labeled_data]
        
        print(f"\n🔧 MEMULAI TRAINING...")
        print(f"   K Value: 5")
        print(f"   Test Size: 20%")
        
        # Initialize classifier
        classifier = KNNClassifier(k=5)
        
        # Prepare data (preprocessing + split)
        print(f"\n   → Preprocessing texts...")
        data = classifier.prepare_data(texts, labels, test_size=0.2, random_state=42)
        
        # Train model
        print(f"   → Training KNN classifier...")
        classifier.train(data['X_train'], data['y_train'])
        
        # Evaluate
        print(f"   → Evaluating model...")
        evaluation = classifier.evaluate(data['X_test'], data['y_test'])
        
        # Save model
        print(f"   → Saving model...")
        classifier.save('models')
        
        result = {
            'success': True,
            'metrics': {
                'accuracy': evaluation['accuracy'],
                'precision': sum(evaluation['precision'].values()) / len(evaluation['precision']),
                'recall': sum(evaluation['recall'].values()) / len(evaluation['recall']),
                'f1_score': sum(evaluation['f1_score'].values()) / len(evaluation['f1_score']),
                'confusion_matrix': evaluation['confusion_matrix']
            }
        }
        
        if result['success']:
            print(f"\n✅ TRAINING BERHASIL!")
            print(f"\n📈 HASIL EVALUASI:")
            print(f"   Accuracy : {result['metrics']['accuracy']:.2%}")
            print(f"   Precision: {result['metrics']['precision']:.2%}")
            print(f"   Recall   : {result['metrics']['recall']:.2%}")
            print(f"   F1 Score : {result['metrics']['f1_score']:.2%}")
            
            print(f"\n💾 MODEL TERSIMPAN:")
            print(f"   File: {os.path.abspath('knn_model.pkl')}")
            
            print(f"\n📊 CONFUSION MATRIX:")
            cm = result['metrics']['confusion_matrix']
            print(f"                Predicted")
            print(f"                RPL    TKJ")
            print(f"   Actual RPL   {cm[0][0]:3d}    {cm[0][1]:3d}")
            print(f"          TKJ   {cm[1][0]:3d}    {cm[1][1]:3d}")
            
        else:
            print(f"\n❌ TRAINING GAGAL!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 70)

if __name__ == '__main__':
    train_model()
