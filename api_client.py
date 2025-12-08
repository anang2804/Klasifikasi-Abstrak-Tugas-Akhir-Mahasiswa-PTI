"""
Client untuk memanggil ML API yang di-deploy terpisah
"""
import requests
from typing import List, Dict
import pandas as pd

class MLAPIClient:
    def __init__(self, api_url: str = "https://your-ml-api.railway.app"):
        self.api_url = api_url
    
    def get_similarity(self, texts: List[str], doc_names: List[str] = None) -> pd.DataFrame:
        """
        Dapatkan similarity matrix dari API
        """
        try:
            response = requests.post(
                f"{self.api_url}/similarity",
                json={"texts": texts, "doc_names": doc_names},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data["similarity_matrix"])
        except Exception as e:
            print(f"Error calling ML API: {e}")
            return pd.DataFrame()
    
    def extract_features(self, texts: List[str]) -> Dict:
        """
        Ekstrak fitur TF-IDF dari API
        """
        try:
            response = requests.post(
                f"{self.api_url}/extract-features",
                json={"texts": texts},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling ML API: {e}")
            return {}
