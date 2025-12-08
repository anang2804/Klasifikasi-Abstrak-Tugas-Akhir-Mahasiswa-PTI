"""
ML API untuk di-deploy terpisah di Railway/Render
"""
from flask import Flask, request, jsonify
from feature_extraction import create_tfidf_features, SimilarityCalculator
import numpy as np

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=5000)
