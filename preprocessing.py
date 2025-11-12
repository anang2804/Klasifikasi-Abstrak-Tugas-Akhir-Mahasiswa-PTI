"""
Modul untuk preprocessing teks Bahasa Indonesia
Meliputi: tokenisasi, stopword removal, dan stemming
"""
import re
import string
from typing import List
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


class TextPreprocessor:
    """Class untuk preprocessing teks Bahasa Indonesia"""
    
    def __init__(self):
        # Inisialisasi stemmer Sastrawi
        stemmer_factory = StemmerFactory()
        self.stemmer = stemmer_factory.create_stemmer()
        
        # Inisialisasi stopword remover Sastrawi
        stopword_factory = StopWordRemoverFactory()
        self.stopword_remover = stopword_factory.create_stop_word_remover()
        
        # Get stopwords list untuk filtering manual jika diperlukan
        self.stopwords = stopword_factory.get_stop_words()
        
        # Tambahan stopwords khusus - HANYA kata-kata yang benar-benar umum/tidak informatif
        additional_stopwords = [
            'abstrak', 'abstract', 'hal', 'vol', 'no', 'issn'
        ]
        self.stopwords.extend(additional_stopwords)
    
    def clean_text(self, text: str) -> str:
        """
        Membersihkan teks dari karakter yang tidak diperlukan
        """
        if not text:
            return ""
        
        # Convert ke lowercase
        text = text.lower()
        
        # Hapus URL
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Hapus email
        text = re.sub(r'\S+@\S+', '', text)
        
        # Hapus angka
        text = re.sub(r'\d+', '', text)
        
        # Hapus tanda baca
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Hapus karakter khusus
        text = re.sub(r'[^\w\s]', '', text)
        
        # Hapus whitespace berlebih
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenisasi teks menjadi list kata
        """
        # Bersihkan teks terlebih dahulu
        text = self.clean_text(text)
        
        # Split berdasarkan whitespace
        tokens = text.split()
        
        # Filter token yang terlalu pendek (< 3 karakter)
        tokens = [token for token in tokens if len(token) >= 3]
        
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Hapus stopwords dari list tokens
        """
        # Filter menggunakan list stopwords
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stopwords
        ]
        
        return filtered_tokens
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """
        Stemming untuk setiap token
        """
        stemmed_tokens = []
        
        for token in tokens:
            # Sastrawi stemmer bekerja pada teks, bukan token individual
            stemmed = self.stemmer.stem(token)
            stemmed_tokens.append(stemmed)
        
        return stemmed_tokens
    
    def preprocess(self, text: str) -> List[str]:
        """
        Pipeline lengkap preprocessing:
        1. Tokenisasi
        2. Stopword removal
        3. Stemming
        
        Returns: List of preprocessed tokens
        """
        # Step 1: Tokenisasi
        tokens = self.tokenize(text)
        
        # Step 2: Hapus stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Step 3: Stemming
        tokens = self.stem_tokens(tokens)
        
        # Filter token kosong jika ada
        tokens = [token for token in tokens if token]
        
        return tokens
    
    def preprocess_to_text(self, text: str) -> str:
        """
        Preprocessing dan return sebagai string (bukan list)
        Berguna untuk beberapa algoritma yang memerlukan input string
        """
        tokens = self.preprocess(text)
        return ' '.join(tokens)
    
    def batch_preprocess(self, texts: List[str]) -> List[List[str]]:
        """
        Preprocessing batch untuk multiple teks
        """
        return [self.preprocess(text) for text in texts]
    
    def batch_preprocess_to_text(self, texts: List[str]) -> List[str]:
        """
        Preprocessing batch dan return sebagai list of strings
        """
        return [self.preprocess_to_text(text) for text in texts]


# Fungsi helper untuk penggunaan cepat
_preprocessor_instance = None

def get_preprocessor() -> TextPreprocessor:
    """
    Singleton pattern untuk text preprocessor
    """
    global _preprocessor_instance
    if _preprocessor_instance is None:
        _preprocessor_instance = TextPreprocessor()
    return _preprocessor_instance


def preprocess_text(text: str) -> List[str]:
    """
    Quick function untuk preprocessing single text
    """
    preprocessor = get_preprocessor()
    return preprocessor.preprocess(text)


def preprocess_texts(texts: List[str]) -> List[List[str]]:
    """
    Quick function untuk preprocessing multiple texts
    """
    preprocessor = get_preprocessor()
    return preprocessor.batch_preprocess(texts)
