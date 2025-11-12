"""
Modul untuk auto-labeling dokumen hasil scraping menggunakan kata kunci berbobot
"""
import re
from typing import Dict, Tuple

# Dictionary kata kunci TKJ dengan bobot
TKJ_KEYWORDS = {
    "routing": 2, "switching": 2, "vlan": 2, "qos": 3, "latency": 2, "packet loss": 3,
    "throughput": 3, "mikrotik": 3, "cisco": 2, "firewall": 2, "ids": 2, "vpn": 2,
    "wlan": 2, "topologi": 2, "sdn": 2, "nfv": 2, "ipv6": 2, "lora": 2, "mqtt": 2,
    "coap": 2, "bandwidth": 2, "server": 1, "virtualisasi": 2, "mesh": 2, "qoe": 2,
    "ethernet": 2, "lan": 2, "wan": 2, "man": 2, "hotspot": 2, "konfigurasi jaringan": 3,
    "ip address": 2, "subnet": 2, "routing static": 2, "routing dynamic": 2,
    "ospf": 3, "rip": 3, "bgp": 3, "dns": 2, "dhcp": 2, "web server": 2, "proxy": 2,
    "load balancing": 2, "monitoring jaringan": 3, "snmp": 2, "wireshark": 2,
    "packet tracer": 2, "ftp": 1, "smtp": 1, "ssh": 1, "iot network": 2,
    "esp32": 2, "arduino": 2, "raspberry pi": 2, "sensor": 2, "gateway": 2,
    "komunikasi data": 3, "wireless": 2, "antena": 2, "keamanan jaringan": 3,
    "jitter": 2, "throughput jaringan": 3, "latency jaringan": 3, "bandwidth usage": 2,
    "trafik jaringan": 3, "pengujian qos": 3, "analisis qos": 3
}

# Dictionary kata kunci RPL dengan bobot
RPL_KEYWORDS = {
    "sdlc": 2, "agile": 2, "scrum": 2, "uml": 2, "erd": 2, "dfd": 2, "use case": 2,
    "activity diagram": 2, "class diagram": 2, "sequence diagram": 2,
    "api": 2, "rest": 2, "restful": 2, "graphql": 2, "json": 1, "microservice": 2,
    "monolith": 1, "database": 2, "basis data": 2, "query": 1, "sql": 1,
    "frontend": 1, "backend": 1, "react": 2, "next.js": 2, "laravel": 2,
    "vue": 2, "angular": 2, "flutter": 2, "android studio": 2, "java": 1,
    "python": 1, "node.js": 2, "express": 2, "typescript": 2, "php": 1,
    "pengujian": 2, "black box": 2, "white box": 2, "unit test": 2, "integrasi": 2,
    "coverage": 2, "sus": 3, "usability": 2, "ui/ux": 2, "antarmuka": 1, "user experience": 2,
    "deploy": 2, "deployment": 2, "ci/cd": 2, "framework": 1,
    "akurasi": 2, "precision": 2, "recall": 2, "f1": 2, "mae": 2, "mse": 2, "rmse": 2,
    "machine learning": 2, "knn": 2, "naive bayes": 2, "decision tree": 2, "svm": 2,
    "clustering": 2, "kmeans": 2, "data mining": 2, "text mining": 2,
    "refactor": 1, "arsitektur": 1, "design pattern": 2, "mvc": 2,
    "sistem informasi": 3, "perangkat lunak": 2, "aplikasi": 3, "prototype": 2,
    "waterfall": 2, "spiral": 2, "incremental": 2, "scrum master": 1, "kanban": 1,
    "useability": 2, "evaluasi sistem": 2, "implementasi aplikasi": 3,
    "pengembangan aplikasi": 3, "pengujian sistem": 3, "dashboard": 2,
    "login": 1, "auth": 1, "token": 1, "jwt": 1, "role": 1, "middleware": 1,
    "web service": 2, "json response": 1, "backend api": 2, "integration": 2,
    "manajemen proyek": 2, "wbs": 1, "gantt": 1, "stakeholder": 1
}


def calculate_keyword_score(text: str, keywords: Dict[str, int]) -> float:
    """
    Menghitung skor berdasarkan kata kunci yang muncul dalam teks
    
    Args:
        text: Teks abstrak (lowercase)
        keywords: Dictionary {keyword: weight}
        
    Returns:
        Total skor berbobot
    """
    text_lower = text.lower()
    total_score = 0.0
    
    for keyword, weight in keywords.items():
        # Cari keyword sebagai whole word (hindari substring false positive)
        # Gunakan regex word boundary
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)
        count = len(matches)
        
        if count > 0:
            # Skor = bobot × jumlah kemunculan (dengan cap agar tidak terlalu dominan)
            # Cap max 3 kemunculan per keyword
            capped_count = min(count, 3)
            total_score += weight * capped_count
    
    return total_score


def auto_label_text(text: str, threshold_ratio: float = 1.2) -> Tuple[str, float]:
    """
    Otomatis memberi label pada teks berdasarkan keyword scoring
    
    Args:
        text: Teks abstrak untuk di-label
        threshold_ratio: Rasio minimum skor untuk confidence tinggi (default 1.2)
        
    Returns:
        Tuple (label: 'RPL'|'TKJ', confidence: 0.0-1.0)
    """
    if not text or len(text.strip()) < 20:
        # Teks terlalu pendek, return default dengan confidence rendah
        return ('RPL', 0.3)
    
    # Hitung skor masing-masing kategori
    score_tkj = calculate_keyword_score(text, TKJ_KEYWORDS)
    score_rpl = calculate_keyword_score(text, RPL_KEYWORDS)
    
    total_score = score_tkj + score_rpl
    
    # Jika tidak ada keyword yang match, default ke RPL dengan confidence rendah
    if total_score == 0:
        return ('RPL', 0.4)
    
    # Tentukan label berdasarkan skor tertinggi
    if score_tkj > score_rpl:
        label = 'TKJ'
        confidence_raw = score_tkj / total_score
        # Boost confidence jika dominan
        if score_tkj > score_rpl * threshold_ratio:
            confidence = min(0.95, confidence_raw + 0.1)
        else:
            confidence = confidence_raw
    else:
        label = 'RPL'
        confidence_raw = score_rpl / total_score
        # Boost confidence jika dominan
        if score_rpl > score_tkj * threshold_ratio:
            confidence = min(0.95, confidence_raw + 0.1)
        else:
            confidence = confidence_raw
    
    # Normalisasi confidence ke range [0.5, 0.95]
    # Keyword-based labeling tidak 100% akurat, jadi cap confidence max 0.95
    confidence = max(0.5, min(0.95, confidence))
    
    return (label, confidence)


def batch_auto_label(texts: list) -> list:
    """
    Auto-label batch teks
    
    Args:
        texts: List of text strings
        
    Returns:
        List of tuples [(label, confidence), ...]
    """
    results = []
    for text in texts:
        label, confidence = auto_label_text(text)
        results.append((label, confidence))
    
    return results


def get_keyword_stats(text: str) -> Dict:
    """
    Mendapatkan statistik keyword yang ditemukan dalam teks
    Berguna untuk debugging dan verifikasi
    
    Args:
        text: Teks abstrak
        
    Returns:
        Dictionary berisi matched keywords per kategori
    """
    text_lower = text.lower()
    
    matched_tkj = []
    matched_rpl = []
    
    # Cari TKJ keywords
    for keyword, weight in TKJ_KEYWORDS.items():
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matched_tkj.append({'keyword': keyword, 'weight': weight})
    
    # Cari RPL keywords
    for keyword, weight in RPL_KEYWORDS.items():
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matched_rpl.append({'keyword': keyword, 'weight': weight})
    
    score_tkj = sum(k['weight'] for k in matched_tkj)
    score_rpl = sum(k['weight'] for k in matched_rpl)
    
    return {
        'tkj_keywords': matched_tkj,
        'rpl_keywords': matched_rpl,
        'score_tkj': score_tkj,
        'score_rpl': score_rpl,
        'predicted_label': 'TKJ' if score_tkj > score_rpl else 'RPL'
    }


# Test function (untuk development)
if __name__ == '__main__':
    # Test cases
    test_texts = [
        "Penelitian ini membahas implementasi routing OSPF dan BGP pada jaringan kampus menggunakan Mikrotik. Pengujian QoS menunjukkan throughput 95 Mbps dengan latency 12ms.",
        "Pengembangan sistem informasi akademik berbasis web menggunakan Laravel dan MySQL. Implementasi menggunakan arsitektur MVC dengan pengujian black box dan usability testing.",
        "Analisis performa jaringan wireless dengan monitoring bandwidth dan jitter menggunakan Wireshark pada topologi mesh."
    ]
    
    print("="*70)
    print("AUTO-LABELING TEST")
    print("="*70)
    
    for i, text in enumerate(test_texts, 1):
        label, confidence = auto_label_text(text)
        stats = get_keyword_stats(text)
        
        print(f"\nTest {i}:")
        print(f"Text: {text[:100]}...")
        print(f"Label: {label} (confidence: {confidence:.2f})")
        print(f"TKJ Score: {stats['score_tkj']} | RPL Score: {stats['score_rpl']}")
        print(f"TKJ Keywords: {[k['keyword'] for k in stats['tkj_keywords'][:5]]}")
        print(f"RPL Keywords: {[k['keyword'] for k in stats['rpl_keywords'][:5]]}")
