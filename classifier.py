"""
Modul untuk klasifikasi menggunakan K-Nearest Neighbor (KNN)
dengan evaluasi model (Precision, Recall, F1-Score)
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, classification_report, confusion_matrix
)
import joblib
import os
from datetime import datetime

from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor


class KNNClassifier:
    """Class untuk klasifikasi dokumen menggunakan KNN"""
    
    def __init__(self, k: int = 5, metric: str = 'cosine'):
        """
        Args:
            k: Jumlah tetangga terdekat
            metric: Metrik jarak ('cosine', 'euclidean', 'manhattan')
        """
        self.k = k
        self.metric = metric
        
        # Inisialisasi KNN classifier
        self.classifier = KNeighborsClassifier(
            n_neighbors=k,
            metric=metric,
            weights='distance'  # Bobot berdasarkan jarak
        )
        
        # Komponen preprocessing dan feature extraction
        self.preprocessor = TextPreprocessor()
        self.feature_extractor = FeatureExtractor()
        
        self.is_trained = False
        self.classes = None
        self.training_info = {}
    
    def prepare_data(self, texts: List[str], labels: List[str], 
                     test_size: float = 0.2, random_state: int = 42) -> Dict:
        """
        Persiapan data untuk training dan testing
        
        Args:
            texts: List of raw texts
            labels: List of labels ('RPL' atau 'TKJ')
            test_size: Proporsi data untuk testing
            random_state: Random seed
            
        Returns:
            Dictionary berisi X_train, X_test, y_train, y_test
        """
        print("Preprocessing texts...")
        # Preprocessing teks
        preprocessed_texts = self.preprocessor.batch_preprocess_to_text(texts)
        
        print("Extracting TF-IDF features...")
        # Extract TF-IDF features
        tfidf_matrix = self.feature_extractor.fit_transform(preprocessed_texts)
        
        print("Splitting data...")
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            tfidf_matrix, labels,
            test_size=test_size,
            random_state=random_state,
            stratify=labels  # Pastikan proporsi kelas seimbang
        )
        
        self.classes = np.unique(labels)
        
        print(f"Training samples: {X_train.shape[0]}")
        print(f"Testing samples: {X_test.shape[0]}")
        print(f"Classes: {self.classes}")
        
        return {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> 'KNNClassifier':
        """
        Train KNN classifier
        
        Args:
            X_train: Training features (TF-IDF matrix)
            y_train: Training labels
        """
        print(f"Training KNN with k={self.k}...")
        
        self.classifier.fit(X_train, y_train)
        self.is_trained = True
        
        # Simpan info training
        self.training_info = {
            'trained_at': datetime.now(),
            'n_samples': X_train.shape[0],
            'n_features': X_train.shape[1],
            'k_value': self.k,
            'metric': self.metric
        }
        
        print("Training completed!")
        
        return self
    
    def predict(self, texts: List[str]) -> np.ndarray:
        """
        Prediksi label untuk teks baru
        
        Args:
            texts: List of raw texts
            
        Returns:
            Array of predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        # Preprocessing
        preprocessed_texts = self.preprocessor.batch_preprocess_to_text(texts)
        
        # Extract features
        tfidf_matrix = self.feature_extractor.transform(preprocessed_texts)
        
        # Predict
        predictions = self.classifier.predict(tfidf_matrix)
        
        return predictions
    
    def predict_proba(self, texts: List[str]) -> np.ndarray:
        """
        Prediksi probabilitas untuk setiap kelas
        
        Returns:
            Array of probability scores
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train.")
        
        # Preprocessing
        preprocessed_texts = self.preprocessor.batch_preprocess_to_text(texts)
        
        # Extract features
        tfidf_matrix = self.feature_extractor.transform(preprocessed_texts)
        
        # Predict probability
        probabilities = self.classifier.predict_proba(tfidf_matrix)
        
        return probabilities
    
    def predict_single(self, text: str) -> Tuple[str, float]:
        """
        Prediksi untuk single text dengan confidence score
        
        Returns:
            Tuple of (predicted_label, confidence)
        """
        predictions = self.predict([text])
        probabilities = self.predict_proba([text])
        
        predicted_label = predictions[0]
        confidence = probabilities[0].max()
        
        return predicted_label, confidence
    
    def get_important_words(self, text: str, top_n: int = 10) -> Dict:
        """
        Mendapatkan kata-kata penting yang mempengaruhi klasifikasi
        
        Args:
            text: Raw text
            top_n: Jumlah kata penting yang ingin diambil
            
        Returns:
            Dictionary dengan kata-kata penting per kelas
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train.")
        
        # Preprocessing
        preprocessed_text = self.preprocessor.preprocess_to_text(text)
        
        # Extract TF-IDF features
        tfidf_vector = self.feature_extractor.transform([preprocessed_text])
        
        # Get feature names
        feature_names = self.feature_extractor.vectorizer.get_feature_names_out()
        
        # Get TF-IDF scores
        tfidf_scores = tfidf_vector.toarray()[0]
        
        # Get top words
        top_indices = tfidf_scores.argsort()[-top_n:][::-1]
        top_words = [(feature_names[i], tfidf_scores[i]) for i in top_indices if tfidf_scores[i] > 0]
        
        # Map preprocessed words to ALL variations in text with improved accuracy
        original_words = []
        
        # Tokenize text more accurately (preserve punctuation boundaries)
        import re
        # Split by whitespace and common punctuation, but keep the words
        words_in_text = re.findall(r'\b\w+\b', text.lower())
        
        for stemmed_word, score in top_words:
            # Find ALL variations of this stemmed word in text
            all_variations = []
            variations_seen = set()
            
            for word in words_in_text:
                # Check if this word stems to our target
                try:
                    word_stem = self.preprocessor.stemmer.stem(word)
                    if word_stem == stemmed_word and word not in variations_seen:
                        all_variations.append(word)
                        variations_seen.add(word)
                except:
                    # Skip words that cause stemming errors
                    continue
            
            # Sort variations by length (prefer longer, more complete forms)
            all_variations.sort(key=len, reverse=True)
            
            # Use longest variation as display, but keep all for highlighting
            display_word = all_variations[0] if all_variations else stemmed_word
            original_words.append({
                'display': display_word,      # Kata untuk ditampilkan di badge
                'stem': stemmed_word,          # Kata setelah stemming
                'variations': all_variations,  # Semua variasi di teks
                'score': score                 # TF-IDF score
            })
        
        return {
            'words': top_words,          # Preprocessed words with scores
            'original_words': original_words,  # Detailed mapping
            'preprocessed_text': preprocessed_text
        }
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluasi model dengan metrik lengkap
        
        Returns:
            Dictionary berisi metrik evaluasi
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train.")
        
        print("Evaluating model...")
        
        # Prediksi
        y_pred = self.classifier.predict(X_test)
        
        # Hitung metrik
        accuracy = accuracy_score(y_test, y_pred)
        
        # Metrik per kelas
        precision = precision_score(y_test, y_pred, average=None, labels=self.classes)
        recall = recall_score(y_test, y_pred, average=None, labels=self.classes)
        f1 = f1_score(y_test, y_pred, average=None, labels=self.classes)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred, labels=self.classes)
        
        # Classification report
        report = classification_report(y_test, y_pred, target_names=self.classes)
        
        print("\n" + "="*50)
        print("EVALUATION RESULTS")
        print("="*50)
        print(f"\nAccuracy: {accuracy:.4f}")
        print(f"\nClassification Report:\n{report}")
        print(f"\nConfusion Matrix:\n{cm}")
        
        # Buat dictionary hasil
        results = {
            'accuracy': accuracy,
            'precision': {self.classes[i]: precision[i] for i in range(len(self.classes))},
            'recall': {self.classes[i]: recall[i] for i in range(len(self.classes))},
            'f1_score': {self.classes[i]: f1[i] for i in range(len(self.classes))},
            'confusion_matrix': cm.tolist(),
            'classification_report': report,
            'n_test_samples': len(y_test)
        }
        
        return results
    
    def cross_validate(self, X: np.ndarray, y: np.ndarray, cv: int = 5) -> Dict:
        """
        Cross-validation untuk evaluasi model
        
        Args:
            X: Features
            y: Labels
            cv: Number of folds
            
        Returns:
            Dictionary berisi CV scores
        """
        print(f"Running {cv}-fold cross-validation...")
        
        scores = cross_val_score(
            self.classifier, X, y,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1
        )
        
        print(f"CV Accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
        
        return {
            'cv_scores': scores.tolist(),
            'mean_accuracy': scores.mean(),
            'std_accuracy': scores.std()
        }
    
    def find_optimal_k(self, X_train: np.ndarray, y_train: np.ndarray,
                       X_test: np.ndarray, y_test: np.ndarray,
                       k_range: range = range(1, 21)) -> Dict:
        """
        Cari nilai k optimal untuk KNN
        
        Returns:
            Dictionary dengan hasil untuk setiap k
        """
        print("Finding optimal k value...")
        
        results = []
        
        for k in k_range:
            # Create temporary classifier
            temp_clf = KNeighborsClassifier(
                n_neighbors=k,
                metric=self.metric,
                weights='distance'
            )
            
            # Train and evaluate
            temp_clf.fit(X_train, y_train)
            y_pred = temp_clf.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            
            results.append({
                'k': k,
                'accuracy': accuracy
            })
            
            print(f"k={k}: Accuracy={accuracy:.4f}")
        
        # Find best k
        best_result = max(results, key=lambda x: x['accuracy'])
        print(f"\nBest k={best_result['k']} with accuracy={best_result['accuracy']:.4f}")
        
        return {
            'results': results,
            'best_k': best_result['k'],
            'best_accuracy': best_result['accuracy']
        }
    
    def save(self, directory: str = 'models'):
        """
        Simpan model, preprocessor, dan feature extractor
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train. Tidak ada yang bisa disimpan.")
        
        os.makedirs(directory, exist_ok=True)
        
        # Simpan classifier
        classifier_path = os.path.join(directory, 'knn_classifier.joblib')
        joblib.dump(self.classifier, classifier_path)
        
        # Simpan feature extractor (vectorizer)
        vectorizer_path = os.path.join(directory, 'tfidf_vectorizer.joblib')
        self.feature_extractor.save(vectorizer_path)
        
        # Simpan metadata
        metadata_path = os.path.join(directory, 'model_metadata.joblib')
        metadata = {
            'k': self.k,
            'metric': self.metric,
            'classes': self.classes,
            'training_info': self.training_info
        }
        joblib.dump(metadata, metadata_path)
        
        print(f"Model saved to {directory}/")
    
    def load(self, directory: str = 'models'):
        """
        Load model dari file
        """
        # Load classifier
        classifier_path = os.path.join(directory, 'knn_classifier.joblib')
        self.classifier = joblib.load(classifier_path)
        
        # Load feature extractor
        vectorizer_path = os.path.join(directory, 'tfidf_vectorizer.joblib')
        self.feature_extractor.load(vectorizer_path)
        
        # Load metadata
        metadata_path = os.path.join(directory, 'model_metadata.joblib')
        metadata = joblib.load(metadata_path)
        
        self.k = metadata['k']
        self.metric = metadata['metric']
        self.classes = metadata['classes']
        self.training_info = metadata['training_info']
        
        self.is_trained = True
        
        print(f"Model loaded from {directory}/")
