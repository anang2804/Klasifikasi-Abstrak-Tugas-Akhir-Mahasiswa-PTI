"""
ML API untuk di-deploy terpisah di Railway/Render
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor, create_tfidf_features, SimilarityCalculator
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model saat startup
MODEL_DIR = 'models'
classifier = None
vectorizer = None
preprocessor = TextPreprocessor()

try:
    if os.path.exists(os.path.join(MODEL_DIR, 'knn_classifier.joblib')):
        classifier = joblib.load(os.path.join(MODEL_DIR, 'knn_classifier.joblib'))
        vectorizer = joblib.load(os.path.join(MODEL_DIR, 'tfidf_vectorizer.joblib'))
        print("✓ Model loaded successfully")
except Exception as e:
    print(f"⚠ Warning: Could not load model - {e}")


@app.route('/')
def home():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'Document Classifier ML API',
        'model_loaded': classifier is not None,
        'endpoints': {
            '/predict': 'POST - Classify document text',
            '/similarity': 'POST - Calculate text similarity',
            '/extract-features': 'POST - Extract TF-IDF features'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': classifier is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint untuk klasifikasi dokumen"""
    if classifier is None or vectorizer is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'Please train the model first'
        }), 503
    
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Preprocess text
        processed_text = preprocessor.preprocess_to_text(text)
        
        # Extract features
        features = vectorizer.transform([processed_text])
        
        # Predict
        prediction = classifier.predict(features)[0]
        probabilities = classifier.predict_proba(features)[0]
        
        # Get class labels
        classes = classifier.classes_
        confidence = {
            str(cls): float(prob) 
            for cls, prob in zip(classes, probabilities)
        }
        
        return jsonify({
            'prediction': str(prediction),
            'confidence': confidence,
            'max_confidence': float(max(probabilities))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/similarity', methods=['POST'])
def calculate_similarity():
    data = request.json
    texts = data.get('texts', [])
    doc_names = data.get('doc_names', None)
    
    if not texts:
        return jsonify({"error": "No texts provided"}), 400
    
    tfidf_matrix, _ = create_tfidf_features(texts)
    similarity_df = SimilarityCalculator.get_similarity_dataframe(tfidf_matrix, doc_names)
    
    return jsonify({
        "similarity_matrix": similarity_df.to_dict()
    })


@app.route('/extract-features', methods=['POST'])
def extract_features():
    data = request.json
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({"error": "No texts provided"}), 400
    
    tfidf_matrix, extractor = create_tfidf_features(texts)
    
    return jsonify({
        "n_features": len(extractor.get_feature_names()),
        "feature_names": extractor.get_feature_names()[:50]
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
