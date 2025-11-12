"""
Modul untuk feature extraction menggunakan TF-IDF dan cosine similarity
"""
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os


class FeatureExtractor:
    """
    Class untuk ekstraksi fitur menggunakan TF-IDF
    
    Implementasi mengikuti rumus:
    - TF(d,t) = f(d,t)  -- kemunculan kata t dalam dokumen d (raw count)
    - IDF(t) = log(N/df(t))  -- N: total dokumen, df(t): dokumen yang memiliki kata t
    - TFIDF = TF(d,t) × IDF(t)
    - Cosine similarity untuk perhitungan jarak antar dokumen
    """
    
    def __init__(self, max_features: int = 1000, ngram_range: Tuple[int, int] = (1, 2)):
        """
        Args:
            max_features: Jumlah maksimal fitur (kata) yang akan digunakan
            ngram_range: Range untuk n-gram (unigram dan bigram)
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        
        # Inisialisasi TF-IDF Vectorizer
        # Sesuai rumus: TF(d,t) = f(d,t) dan IDF(t) = log(N/df(t))
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=2,  # Minimal muncul di 2 dokumen
            max_df=0.8,  # Maksimal muncul di 80% dokumen
            sublinear_tf=False,  # TF(d,t) = f(d,t) - raw count, bukan logaritmik
            use_idf=True,  # Gunakan IDF: log(N/df(t))
            smooth_idf=True,  # IDF = log((N+1)/(df(t)+1)) + 1 untuk hindari divide-by-zero
            norm='l2'  # Normalisasi L2 untuk cosine similarity
        )
        
        self.is_fitted = False
        self.feature_names = None
    
    def fit(self, texts: List[str]) -> 'FeatureExtractor':
        """
        Fit vectorizer pada corpus teks
        
        Args:
            texts: List of preprocessed texts (as strings)
        """
        self.vectorizer.fit(texts)
        self.is_fitted = True
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        print(f"TF-IDF Vectorizer fitted with {len(self.feature_names)} features")
        
        return self
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform teks menjadi TF-IDF vectors
        
        Args:
            texts: List of preprocessed texts
            
        Returns:
            TF-IDF matrix (sparse matrix)
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer belum di-fit. Jalankan fit() terlebih dahulu.")
        
        tfidf_matrix = self.vectorizer.transform(texts)
        return tfidf_matrix
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """
        Fit dan transform sekaligus
        """
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.is_fitted = True
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        print(f"TF-IDF Vectorizer fitted with {len(self.feature_names)} features")
        
        return tfidf_matrix
    
    def get_feature_names(self) -> List[str]:
        """
        Dapatkan nama-nama fitur (kata-kata)
        """
        if not self.is_fitted:
            return []
        return list(self.feature_names)
    
    def get_top_features(self, tfidf_vector: np.ndarray, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Dapatkan top-N fitur dengan bobot TF-IDF tertinggi dari sebuah dokumen
        
        Args:
            tfidf_vector: TF-IDF vector untuk satu dokumen
            top_n: Jumlah top features yang ingin ditampilkan
            
        Returns:
            List of (feature_name, tfidf_score) tuples
        """
        if not self.is_fitted:
            return []
        
        # Jika input sparse matrix, convert ke array
        if hasattr(tfidf_vector, 'toarray'):
            tfidf_vector = tfidf_vector.toarray().flatten()
        else:
            tfidf_vector = tfidf_vector.flatten()
        
        # Dapatkan indices dengan score tertinggi
        top_indices = tfidf_vector.argsort()[-top_n:][::-1]
        
        # Dapatkan feature names dan scores
        top_features = [
            (self.feature_names[i], tfidf_vector[i])
            for i in top_indices
            if tfidf_vector[i] > 0
        ]
        
        return top_features
    
    def save(self, filepath: str):
        """
        Simpan vectorizer ke file
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer belum di-fit. Tidak ada yang bisa disimpan.")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.vectorizer, filepath)
        print(f"Vectorizer saved to {filepath}")
    
    def load(self, filepath: str):
        """
        Load vectorizer dari file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} tidak ditemukan")
        
        self.vectorizer = joblib.load(filepath)
        self.is_fitted = True
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        print(f"Vectorizer loaded from {filepath}")


class SimilarityCalculator:
    """
    Class untuk menghitung similarity antar dokumen
    
    Implementasi Cosine Similarity sesuai rumus:
    cos(x,y) = (x·y) / (||x|| ||y||)
    
    Dimana:
    - x·y = Σ(x_k × y_k)  -- dot product
    - ||x|| = sqrt(Σ x_k²)  -- panjang vektor x
    - ||y|| = sqrt(Σ y_k²)  -- panjang vektor y
    """
    
    @staticmethod
    def cosine_similarity_matrix(tfidf_matrix: np.ndarray) -> np.ndarray:
        """
        Hitung cosine similarity antar semua dokumen
        
        Args:
            tfidf_matrix: TF-IDF matrix dari semua dokumen
            
        Returns:
            Similarity matrix (n_documents x n_documents)
        """
        return cosine_similarity(tfidf_matrix)
    
    @staticmethod
    def cosine_similarity_pair(vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        Hitung cosine similarity antara dua vector
        
        Args:
            vector1: TF-IDF vector dokumen pertama
            vector2: TF-IDF vector dokumen kedua
            
        Returns:
            Cosine similarity score (0-1)
        """
        # Reshape jika perlu
        if len(vector1.shape) == 1:
            vector1 = vector1.reshape(1, -1)
        if len(vector2.shape) == 1:
            vector2 = vector2.reshape(1, -1)
        
        return cosine_similarity(vector1, vector2)[0][0]
    
    @staticmethod
    def find_k_nearest(query_vector: np.ndarray, 
                       document_vectors: np.ndarray, 
                       k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Temukan k dokumen terdekat dari query
        
        Args:
            query_vector: TF-IDF vector dari query
            document_vectors: TF-IDF matrix dari semua dokumen
            k: Jumlah nearest neighbors
            
        Returns:
            Tuple of (indices, similarities)
        """
        # Hitung similarity dengan semua dokumen
        similarities = cosine_similarity(query_vector, document_vectors)[0]
        
        # Dapatkan k indices dengan similarity tertinggi
        k_nearest_indices = similarities.argsort()[-k:][::-1]
        k_nearest_similarities = similarities[k_nearest_indices]
        
        return k_nearest_indices, k_nearest_similarities
    
    @staticmethod
    def get_similarity_dataframe(tfidf_matrix: np.ndarray, 
                                 document_names: List[str] = None) -> pd.DataFrame:
        """
        Buat DataFrame similarity matrix untuk visualisasi
        
        Args:
            tfidf_matrix: TF-IDF matrix
            document_names: Nama-nama dokumen (opsional)
            
        Returns:
            DataFrame dengan similarity scores
        """
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        if document_names is None:
            document_names = [f"Doc_{i}" for i in range(len(similarity_matrix))]
        
        return pd.DataFrame(
            similarity_matrix,
            index=document_names,
            columns=document_names
        )


# Fungsi helper
def create_tfidf_features(texts: List[str], 
                         max_features: int = 1000,
                         ngram_range: Tuple[int, int] = (1, 2)) -> Tuple[np.ndarray, FeatureExtractor]:
    """
    Helper function untuk membuat TF-IDF features
    
    Returns:
        Tuple of (tfidf_matrix, feature_extractor)
    """
    extractor = FeatureExtractor(max_features=max_features, ngram_range=ngram_range)
    tfidf_matrix = extractor.fit_transform(texts)
    
    return tfidf_matrix, extractor
