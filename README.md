# Klasifikasi Abstrak Tugas Akhir Mahasiswa PTI Berdasarkan Bidang Keahlian Menggunakan K-Nearest Neighbor (KNN)

## Deskripsi

Website ini mengklasifikasikan abstrak tugas akhir mahasiswa Program Studi PTI ke dalam dua kategori utama:

- **Rekayasa Perangkat Lunak (RPL)**
- **Teknik Komputer dan Jaringan (TKJ)**

## Fitur Utama

- ✅ Web scraping otomatis dari ejournal.unesa.ac.id (2020-2025)
- ✅ **Auto-labeling dengan keyword scoring** (130+ keywords: 60 TKJ, 70 RPL dengan bobot 1-3)
- ✅ **Smart abstract extraction** - hanya ekstrak bagian abstrak dari PDF/DOCX (bukan seluruh dokumen)
- ✅ **Tracking data uji terpisah** - ClassificationHistory untuk hasil klasifikasi
- ✅ Preprocessing teks Bahasa Indonesia (tokenisasi, stopword removal, stemming Sastrawi)
- ✅ Feature extraction dengan TF-IDF (sesuai rumus matematis TF-IDF)
- ✅ Klasifikasi dokumen menggunakan algoritma K-Nearest Neighbor (KNN, k=5, cosine similarity)
- ✅ Upload file multi-format (TXT, PDF, DOCX) dengan ekstraksi otomatis
- ✅ Evaluasi model dengan metrik Precision, Recall, F1-Score, dan Confusion Matrix
- ✅ Visualisasi hasil klasifikasi dalam bentuk grafik dan statistik
- ✅ Dokumentasi lengkap rumus matematis dan implementasi

## Teknologi

- **Backend**: Flask 3.0.0 (Python 3.8+)
- **Machine Learning**: scikit-learn 1.3+ (KNN, TF-IDF Vectorizer)
- **Text Processing**: Sastrawi 1.2.0 (Stemming Nazief-Adriani), NLTK (Tokenization)
- **File Processing**: PyPDF2 3.0.0 (PDF), python-docx 1.2.0 (DOCX)
- **Web Scraping**: BeautifulSoup4, Requests
- **Database**: SQLite dengan SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js, Font Awesome

## Instalasi

### 1. Clone repository atau extract project

### 2. Buat virtual environment

```bash
python -m venv venv
```

### 3. Aktivasi virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup environment variables

```bash
cp .env.example .env
```

### 6. Download NLTK data

```bash
python -c "import nltk; nltk.download('punkt')"
```

### 7. Jalankan aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Penggunaan

### 1. Scraping Data

- Akses halaman `/scrape` untuk melakukan scraping data dari ejournal.unesa.ac.id
- **Data otomatis dilabeli saat scraping** menggunakan keyword scoring (130+ keywords)
- Label ditentukan berdasarkan:
  - **TKJ Keywords** (60+): jaringan, komputer, router, cisco, mikrotik, server, hardware, dll (bobot 1-3)
  - **RPL Keywords** (70+): aplikasi, software, web, android, sistem informasi, database, dll (bobot 1-3)
- Confidence score dihitung dari rasio skor keyword terbesar vs total
- Semua data hasil scraping tersimpan di **Data Latih** dengan label otomatis

### 2. Mengelola Data Latih

- Akses menu **Data → Data Latih** untuk melihat data training
- Tampilan tabel dengan kolom: Judul, Penulis, Tahun, Abstrak, Label (RPL/TKJ)
- Statistik: Total data, jumlah RPL, jumlah TKJ, distribusi persentase
- Data latih digunakan untuk melatih model KNN
- Minimal 10 data berlabel diperlukan untuk training

### 3. Training Model

- Akses halaman `/train` untuk melatih model KNN
- Proses training:
  1. Preprocessing: Tokenizing → Stopword Removal → Stemming
  2. TF-IDF Vectorization (max_features=1000, ngram_range=(1,2))
  3. KNN Training (k=5, metric='cosine', weights='distance')
- Model disimpan: `knn_classifier.joblib`, `tfidf_vectorizer.joblib`
- Evaluasi otomatis dengan train-test split (80:20)

### 4. Klasifikasi Abstrak Baru

**Opsi 1: Input Manual**
- Akses halaman `/classify`
- Copy-paste teks abstrak ke text area
- Klik "Klasifikasi" untuk mendapat prediksi (RPL/TKJ) + confidence score
- Hasil tersimpan di **Data Uji** dengan sumber "Manual Input"

**Opsi 2: Upload File**
- Mendukung 3 format: TXT, PDF, DOCX
- **Smart extraction**: Hanya ekstrak bagian ABSTRAK (bukan seluruh dokumen)
- PDF: Maksimal 15 halaman pertama, cari pattern "ABSTRAK"
- DOCX: Baca paragraph-per-paragraph, berhenti setelah menemukan abstrak
- Hasil tersimpan di **Data Uji** dengan sumber "File Upload"

### 5. Mengelola Data Uji

- Akses menu **Data → Data Uji** untuk melihat history klasifikasi
- Tampilan tabel dengan kolom: Teks Abstrak, Prediksi, Confidence, Sumber, Waktu
- Statistik: Total, RPL, TKJ, Manual Input, File Upload
- Fitur: Hapus data individual atau hapus semua data uji
- Data uji terpisah dari data latih (model ClassificationHistory)

### 6. Evaluasi Model

- Akses halaman `/evaluation` untuk melihat performa model
- Metrik: Accuracy, Precision, Recall, F1-Score (per kelas)
- Confusion Matrix untuk analisis error
- Grafik distribusi data training dan testing
- Statistik: Jumlah sampel training, testing, waktu training

## Dokumentasi Lengkap

Project ini dilengkapi dengan dokumentasi teknis yang komprehensif:

- **RUMUS_MATEMATIKA.md**: Penjelasan detail semua formula matematis (TF-IDF, Cosine Similarity, KNN) dengan notasi LaTeX
- **RUMUS_SEDERHANA.md**: Penjelasan user-friendly dengan contoh kasus dan FAQ
- **GUIDE.md**: Panduan lengkap arsitektur sistem dan pengembangan
- **TFIDF_IMPLEMENTATION.md**: Detail implementasi TF-IDF sesuai paper penelitian

## Database Schema

### Model: Abstract (Data Latih)
```python
- id: Integer (Primary Key)
- title: String(500)
- author: String(200)
- year: Integer
- abstract_text: Text
- url: String(500)
- label: String(10)  # 'RPL' atau 'TKJ'
- predicted_label: String(10)
- confidence: Float
- is_training_data: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### Model: ClassificationHistory (Data Uji)
```python
- id: Integer (Primary Key)
- abstract_text: Text
- predicted_label: String(10)  # 'RPL' atau 'TKJ'
- confidence: Float
- source: String(20)  # 'manual' atau 'upload'
- classified_at: DateTime
```

### Model: ModelMetrics
```python
- id: Integer (Primary Key)
- accuracy: Float
- precision_rpl: Float
- precision_tkj: Float
- recall_rpl: Float
- recall_tkj: Float
- f1_rpl: Float
- f1_tkj: Float
- confusion_matrix: Text (JSON)
- training_samples: Integer
- test_samples: Integer
- trained_at: DateTime
```

## Struktur File Project

```
doc-classifier/
├── app.py                          # Main Flask application
├── models.py                       # Database models (SQLAlchemy)
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
│
├── auto_labeler.py                 # Auto-labeling dengan keyword scoring
├── scraper.py                      # Web scraper untuk ejournal.unesa.ac.id
├── preprocessing.py                # Text preprocessing (tokenize, stopword, stem)
├── feature_extraction.py           # TF-IDF implementation
├── classifier.py                   # KNN classifier
├── utils.py                        # Helper functions
│
├── init_db.py                      # Database initialization
├── scrape_now.py                   # Quick scraping script
├── train_now.py                    # Quick training script
├── auto_label_existing.py          # Batch auto-label existing data
│
├── test_*.py                       # Testing scripts
├── run.sh / run.bat                # Run scripts
│
├── templates/                      # HTML templates (Jinja2)
│   ├── base.html                   # Base template dengan navbar
│   ├── index.html                  # Dashboard/Beranda
│   ├── scrape.html                 # Scraping interface
│   ├── label_data.html             # Data latih (training data)
│   ├── test_data.html              # Data uji (classification history)
│   ├── train.html                  # Training interface
│   ├── classify.html               # Classification interface
│   └── evaluation.html             # Evaluation metrics
│
├── models/                         # Trained model files (gitignored)
│   ├── knn_classifier.joblib
│   ├── tfidf_vectorizer.joblib
│   └── model_metadata.joblib
│
├── instance/                       # Database files (gitignored)
│   └── abstracts.db
│
├── uploads/                        # Uploaded files (gitignored)
│
└── Documentation files:
    ├── README.md
    ├── GUIDE.md
    ├── RUMUS_MATEMATIKA.md
    ├── RUMUS_SEDERHANA.md
    └── TFIDF_IMPLEMENTATION.md
```

## Referensi

Alfian Sukma, Badrus Zaman, Endah Purwanti (2015). "Klasifikasi Dokumen Temu Kembali Informasi dengan K-Nearest Neighbor"

## Alur Proses Sistem

### 1. Alur Proses Training Sistem (Update Implementasi Terbaru)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          TRAINING PIPELINE                          │
└─────────────────────────────────────────────────────────────────────┘

START
  ↓
┌──────────────────────────┐
│  1. WEB SCRAPING         │ → ejournal.unesa.ac.id (2020-2025)
│  (Menu: Scraping)        │
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│  2. AUTO-LABELING        │ → Keyword Scoring (130+ keywords)
│  (auto_labeler.py)       │   - TKJ: 60 keywords (bobot 1-3)
└──────────────────────────┘   - RPL: 70 keywords (bobot 1-3)
  ↓                             → Confidence calculation
┌──────────────────────────┐   → Label: RPL atau TKJ
│  3. DATA LATIH           │
│  (Model: Abstract)       │ → Simpan ke database dengan label
│  (Menu: Data Latih)      │   → Total: 312 data (242 RPL, 70 TKJ)
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│  4. TRAINING MODEL       │ → Train-Test Split (80:20)
│  (Menu: Training)        │
└──────────────────────────┘
  ↓
  ├─→ ┌──────────────────────────┐
  │   │ 4a. TEXT PREPROCESSING   │ → Tokenizing (case folding, clean)
  │   │ (preprocessing.py)       │ → Stopword Removal (~750 words)
  │   └──────────────────────────┘ → Stemming (Nazief-Adriani)
  │
  ├─→ ┌──────────────────────────┐
  │   │ 4b. FEATURE EXTRACTION   │ → TF-IDF Vectorization
  │   │ (feature_extraction.py)  │   - TF(d,t) = f(d,t) (raw count)
  │   └──────────────────────────┘   - IDF = log((N+1)/(df+1))+1
  │                                   - L2 Normalization
  │                                   - Output: 1000 features
  │
  ├─→ ┌──────────────────────────┐
  │   │ 4c. KNN TRAINING         │ → k=5 nearest neighbors
  │   │ (classifier.py)          │ → metric='cosine'
  │   └──────────────────────────┘ → weights='distance'
  │
  └─→ ┌──────────────────────────┐
      │ 4d. MODEL EVALUATION     │ → Accuracy, Precision, Recall
      │ (evaluate method)        │ → F1-Score, Confusion Matrix
      └──────────────────────────┘ → Simpan ke ModelMetrics
  ↓
┌──────────────────────────┐
│  5. SAVE MODEL           │ → knn_classifier.joblib
│  (models/ directory)     │ → tfidf_vectorizer.joblib
└──────────────────────────┘ → model_metadata.joblib
  ↓
END (Model siap untuk klasifikasi)
```

**Mapping ke Menu Website:**

| Tahap                  | Menu Website      | File/Modul                  | Keterangan                                   |
| ---------------------- | ----------------- | --------------------------- | -------------------------------------------- |
| **Web Scraping**       | Menu Scraping     | `scraper.py`                | Scrape 100+ abstrak dari ejournal            |
| **Auto-Labeling**      | Auto saat Scrape  | `auto_labeler.py`           | Keyword scoring → RPL/TKJ (confidence)       |
| **Data Latih**         | Menu Data Latih   | `templates/label_data.html` | View 312 data dengan auto-label              |
| **Training**           | Menu Training     | `templates/train.html`      | Trigger training pipeline                    |
| **Text Preprocessing** | Auto di Training  | `preprocessing.py`          | Clean → Tokenize → Stopword → Stem           |
| **TF-IDF**             | Auto di Training  | `feature_extraction.py`     | Vectorization (1000 features, L2 norm)       |
| **KNN**                | Auto di Training  | `classifier.py`             | Train model (k=5, cosine similarity)         |
| **Evaluation**         | Auto di Training  | `classifier.py` (evaluate)  | Hitung metrik → Simpan ke database           |
| **View Metrics**       | Menu Evaluasi     | `templates/evaluation.html` | Tampilkan accuracy, precision, recall, F1    |
| **Data Uji**           | Menu Data Uji     | `templates/test_data.html`  | History klasifikasi (manual + upload)        |

### 2. Alur Proses Text Mining (Preprocessing)

```
START
  ↓
Tokenizing (Case Folding & Split)
  ↓
Filtering (Stopword Removal)
  ↓
Stemming (Sastrawi)
  ↓
END
```

**Detail Implementasi di `preprocessing.py`:**

1. **Tokenizing** → `tokenize()`
   - Case folding (huruf kecil semua)
   - Hapus URL, email, angka, tanda baca
   - Split berdasarkan whitespace
   - Filter token minimal 3 karakter
2. **Filtering** → `remove_stopwords()`
   - Hapus kata umum Bahasa Indonesia ("yang", "di", "ke", "dari", "dan", dll)
   - Stopwords: Sastrawi + custom ("abstrak", "hal", "vol", "issn")
3. **Stemming** → `stem_tokens()`
   - Konversi kata ke bentuk dasar menggunakan Sastrawi Stemmer
   - Contoh: "menggunakan" → "guna", "pembelajaran" → "ajar"

**Contoh Proses:**

```
Input   : "Penelitian ini bertujuan untuk mengembangkan sistem informasi"
Tokenize: ["penelitian", "ini", "bertujuan", "untuk", "mengembangkan", "sistem", "informasi"]
Filter  : ["penelitian", "bertujuan", "mengembangkan", "sistem", "informasi"]
Stem    : ["teliti", "tuju", "kembang", "sistem", "informasi"]
```

### 3. Alur Proses K-Nearest Neighbor (Klasifikasi)

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CLASSIFICATION PIPELINE                        │
└─────────────────────────────────────────────────────────────────────┘

START (Abstrak baru dari user)
  ↓
┌──────────────────────────┐
│  1. INPUT ABSTRAK        │ → Manual Input (text area)
│  (Menu: Klasifikasi)     │ → Upload File (TXT/PDF/DOCX)
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│  2. SMART EXTRACTION     │ → TXT: Pattern matching "ABSTRAK"
│  (untuk upload file)     │ → PDF: Max 15 halaman, cari "ABSTRAK"
│  (extract_abstract_      │ → DOCX: Paragraph-by-paragraph
│   section)               │ → Output: Teks abstrak saja (bukan full doc)
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│  3. TEXT PREPROCESSING   │ → Tokenizing (clean + split)
│  (preprocessing.py)      │ → Stopword Removal
└──────────────────────────┘ → Stemming (Sastrawi)
  ↓
┌──────────────────────────┐
│  4. TF-IDF TRANSFORM     │ → Load tfidf_vectorizer.joblib
│  (feature_extraction.py) │ → Transform text ke vektor (1000 features)
└──────────────────────────┘ → Normalisasi L2
  ↓
┌──────────────────────────┐
│  5. LOAD KNN MODEL       │ → Load knn_classifier.joblib
│  (classifier.py)         │ → Model sudah trained dengan data latih
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│  6. HITUNG COSINE        │ → Cosine Similarity = (A·B)/(||A||×||B||)
│     SIMILARITY           │ → Hitung dengan semua data training
└──────────────────────────┘ → Urutkan dari tertinggi ke terendah
  ↓
┌──────────────────────────┐
│  7. AMBIL k-NN           │ → Ambil 5 dokumen terdekat (k=5)
│     (k=5)                │ → Contoh: [RPL:0.85, RPL:0.82, TKJ:0.78,
└──────────────────────────┘           RPL:0.75, TKJ:0.72]
  ↓
┌──────────────────────────┐
│  8. VOTING MAYORITAS     │
└──────────────────────────┘
  ↓
  Terdapat kategori mayoritas?
  │
  ├─ YES (Mayoritas Jelas) ──→ ┌──────────────────────────┐
  │                             │  9a. AMBIL LABEL         │
  │                             │      MAYORITAS           │
  │                             └──────────────────────────┘
  │                             Contoh: [RPL, RPL, RPL, TKJ, RPL]
  │                             → Label: RPL
  │                             → Confidence: 4/5 = 80%
  │
  └─ NO (Voting Seri 2:2:1) ─→ ┌──────────────────────────┐
                                │  9b. AMBIL DARI DOKUMEN  │
                                │      SIMILARITY TERTINGGI│
                                └──────────────────────────┘
                                Contoh: [RPL:0.85, RPL:0.82, 
                                         TKJ:0.78, TKJ:0.77]
                                → Label: RPL (similarity 0.85)
                                → Confidence: 2/4 = 50%
  ↓
┌──────────────────────────┐
│  10. OUTPUT HASIL        │ → Label: RPL atau TKJ
│                          │ → Confidence: 50% - 100%
│                          │ → Top 20 kata kunci (TF-IDF tertinggi)
│                          │ → Highlight kata penting di teks
└──────────────────────────┘
  ↓
┌──────────────────────────┐
│  11. SIMPAN KE DATA UJI  │ → Model: ClassificationHistory
│  (Menu: Data Uji)        │ → Fields: abstract_text, predicted_label,
└──────────────────────────┘           confidence, source, classified_at
  ↓
END (Hasil klasifikasi ditampilkan)
```

**File Implementasi:**

| Komponen              | File/Function                  | Output                          |
| --------------------- | ------------------------------ | ------------------------------- |
| Input Interface       | `templates/classify.html`      | Form input + upload             |
| Smart Extraction      | `app.py: extract_abstract_section()` | Teks abstrak saja        |
| Preprocessing         | `preprocessing.py: preprocess_text()` | Token yang di-stem      |
| TF-IDF Transform      | `feature_extraction.py: transform()` | Vektor 1000 features     |
| KNN Prediction        | `classifier.py: predict_single()` | Label + confidence          |
| Save to DB            | `app.py: /classify route`      | Insert ClassificationHistory    |
| Display Result        | `templates/classify.html`      | Prediksi + keyword + highlight  |

## Metode dan Algoritma

### 1. Auto-Labeling (Keyword Scoring)
- **TKJ Keywords** (60+ terms): jaringan, router, cisco, mikrotik, server, hardware, dll
- **RPL Keywords** (70+ terms): aplikasi, web, android, sistem informasi, database, dll
- **Weighted Scoring**: Setiap keyword memiliki bobot 1-3 berdasarkan spesifisitas
- **Algorithm**: 
  ```
  TKJ_Score = Σ(weight × min(count, 3))
  RPL_Score = Σ(weight × min(count, 3))
  Label = argmax(TKJ_Score, RPL_Score)
  Confidence = max_score / (TKJ_Score + RPL_Score)
  ```

### 2. Text Preprocessing (Sastrawi + NLTK)
- **Tokenisasi**: Case folding, remove URL/email/numbers, split whitespace
- **Stopword Removal**: ~750 stopwords Bahasa Indonesia (Sastrawi + custom)
- **Stemming**: Algoritma Nazief-Adriani (Sastrawi Stemmer)
- **Example**: "menggunakan" → "guna", "pembelajaran" → "ajar"

### 3. Feature Extraction (TF-IDF)
- **Formula**: TF(d,t) = f(d,t), IDF(t) = log((N+1)/(df+1)) + 1
- **Parameters**: 
  - `max_features=1000`: Ambil 1000 kata paling penting
  - `ngram_range=(1,2)`: Unigram + bigram
  - `min_df=2, max_df=0.8`: Filter kata terlalu jarang/umum
  - `sublinear_tf=False`: Raw count (sesuai rumus)
  - `use_idf=True, norm='l2'`: Normalisasi L2

### 4. K-Nearest Neighbor (KNN)
- **Parameters**: k=5, metric='cosine', weights='distance'
- **Cosine Similarity**: sim(A,B) = (A·B) / (||A|| × ||B||)
- **Classification**: Voting mayoritas dari 5 tetangga terdekat
- **Confidence**: Persentase voting kelas mayoritas

### 5. Evaluation Metrics
- **Accuracy**: (TP + TN) / Total
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)
- **Confusion Matrix**: Visualisasi prediksi vs aktual

## Alur Proses Detail dengan Rumus

### Alur 4: Proses Evaluasi Model (Metrik Performa)

```
┌─────────────────────────────────────────────────────────────────────┐
│                       EVALUATION PIPELINE                           │
└─────────────────────────────────────────────────────────────────────┘

START (Setelah Training Model)
  ↓
┌──────────────────────────┐
│  1. TRAIN-TEST SPLIT     │ → Data Latih (312 data)
│  (80:20)                 │   ├─ Training Set: 249 data (80%)
└──────────────────────────┘   └─ Testing Set: 63 data (20%)
  ↓
┌──────────────────────────┐
│  2. MODEL PREDICTION     │ → KNN predict pada testing set
│  (pada test set)         │ → Output: y_pred = [RPL, TKJ, RPL, ...]
└──────────────────────────┘ → Bandingkan dengan y_true (label asli)
  ↓
┌──────────────────────────┐
│  3. CONFUSION MATRIX     │
└──────────────────────────┘
  
                    Predicted
                 RPL      TKJ
         ┌─────────────────────┐
     RPL │  TP_rpl  │  FN_rpl  │  → True Positive RPL, False Negative RPL
Actual   ├─────────────────────┤
     TKJ │  FP_rpl  │  TP_tkj  │  → False Positive RPL, True Positive TKJ
         └─────────────────────┘
  
  Contoh Real:
                 RPL    TKJ
          ┌──────────────────┐
      RPL │  45    │   3     │  → 45 benar RPL, 3 salah prediksi TKJ
      TKJ │   2    │  13     │  → 2 salah prediksi RPL, 13 benar TKJ
          └──────────────────┘
  
  ↓
┌──────────────────────────────────────────────────────────────────┐
│  4. HITUNG METRIK EVALUASI                                       │
└──────────────────────────────────────────────────────────────────┘
```

#### 4a. ACCURACY (Akurasi Keseluruhan)

**Formula:**
```
Accuracy = (TP_rpl + TP_tkj) / Total_Prediksi
         = (Jumlah Prediksi Benar) / (Total Semua Prediksi)
```

**Contoh Perhitungan:**
```
TP_rpl = 45   (Prediksi RPL, Actual RPL - BENAR)
TP_tkj = 13   (Prediksi TKJ, Actual TKJ - BENAR)
FP_rpl = 2    (Prediksi RPL, Actual TKJ - SALAH)
FN_rpl = 3    (Prediksi TKJ, Actual RPL - SALAH)

Accuracy = (45 + 13) / (45 + 13 + 2 + 3)
         = 58 / 63
         = 0.9206 = 92.06%
```

**Interpretasi:**
- Model benar mengklasifikasi **92.06%** dari semua data test
- Semakin tinggi accuracy, semakin baik model secara keseluruhan
- Cocok digunakan ketika dataset **seimbang** (jumlah RPL ≈ TKJ)

---

#### 4b. PRECISION (Presisi per Kelas)

**Formula:**
```
Precision_RPL = TP_rpl / (TP_rpl + FP_rpl)
              = (Prediksi RPL yang Benar) / (Semua yang Diprediksi RPL)

Precision_TKJ = TP_tkj / (TP_tkj + FP_tkj)
              = (Prediksi TKJ yang Benar) / (Semua yang Diprediksi TKJ)
```

**Contoh Perhitungan:**
```
Precision_RPL = 45 / (45 + 2) 
              = 45 / 47 
              = 0.9574 = 95.74%

Precision_TKJ = 13 / (13 + 3) 
              = 13 / 16 
              = 0.8125 = 81.25%
```

**Interpretasi:**
- Dari semua yang diprediksi **RPL**, **95.74%** benar-benar RPL
- Dari semua yang diprediksi **TKJ**, **81.25%** benar-benar TKJ
- **Precision tinggi** = sedikit **False Positive** (salah prediksi positif)
- Penting ketika cost dari False Positive tinggi

---

#### 4c. RECALL (Sensitivitas/Daya Ingat per Kelas)

**Formula:**
```
Recall_RPL = TP_rpl / (TP_rpl + FN_rpl)
           = (Prediksi RPL yang Benar) / (Semua yang Seharusnya RPL)

Recall_TKJ = TP_tkj / (TP_tkj + FN_tkj)
           = (Prediksi TKJ yang Benar) / (Semua yang Seharusnya TKJ)
```

**Contoh Perhitungan:**
```
Recall_RPL = 45 / (45 + 3) 
           = 45 / 48 
           = 0.9375 = 93.75%

Recall_TKJ = 13 / (13 + 2) 
           = 13 / 15 
           = 0.8667 = 86.67%
```

**Interpretasi:**
- Dari semua abstrak **RPL asli**, **93.75%** berhasil terdeteksi sebagai RPL
- Dari semua abstrak **TKJ asli**, **86.67%** berhasil terdeteksi sebagai TKJ
- **Recall tinggi** = sedikit **False Negative** (data tidak terdeteksi)
- Penting ketika cost dari False Negative tinggi (miss detection)

---

#### 4d. F1-SCORE (Harmonic Mean dari Precision & Recall)

**Formula:**
```
F1_RPL = 2 × (Precision_RPL × Recall_RPL) / (Precision_RPL + Recall_RPL)

F1_TKJ = 2 × (Precision_TKJ × Recall_TKJ) / (Precision_TKJ + Recall_TKJ)
```

**Contoh Perhitungan:**
```
F1_RPL = 2 × (0.9574 × 0.9375) / (0.9574 + 0.9375)
       = 2 × 0.8976 / 1.8949
       = 0.9474 = 94.74%

F1_TKJ = 2 × (0.8125 × 0.8667) / (0.8125 + 0.8667)
       = 2 × 0.7042 / 1.6792
       = 0.8387 = 83.87%
```

**Interpretasi:**
- F1-Score adalah **rata-rata harmonis** dari Precision dan Recall
- Nilai tinggi (mendekati 100%) = model **balance** antara precision & recall
- **F1_RPL 94.74%** = model sangat baik untuk kelas RPL
- **F1_TKJ 83.87%** = model cukup baik untuk kelas TKJ
- Digunakan ketika ingin **keseimbangan** antara precision dan recall

---

```
  ↓
┌──────────────────────────┐
│  5. SIMPAN METRICS       │ → Model: ModelMetrics
│  (ke database)           │ → Fields: accuracy, precision_rpl, 
└──────────────────────────┘   precision_tkj, recall_rpl, recall_tkj,
  ↓                             f1_rpl, f1_tkj, confusion_matrix,
┌──────────────────────────┐   training_samples, test_samples, trained_at
│  6. VISUALISASI          │
│  (Menu: Evaluasi)        │ → Grafik Confusion Matrix (heatmap)
└──────────────────────────┘ → Grafik Bar Chart (Precision, Recall, F1)
  ↓                             → Tabel Metrik per Kelas
END                             → Statistik Training/Testing Samples
```

---

### Rangkuman Metrik Evaluasi

| Metrik      | Formula                          | Interpretasi                              | Range  | Kapan Digunakan |
| ----------- | -------------------------------- | ----------------------------------------- | ------ | --------------- |
| **Accuracy**| (TP+TN) / Total                  | Akurasi keseluruhan model                 | 0-100% | Dataset seimbang |
| **Precision**| TP / (TP + FP)                  | Ketepatan prediksi positif                | 0-100% | False Positive berbahaya |
| **Recall**  | TP / (TP + FN)                   | Kemampuan mendeteksi kelas positif        | 0-100% | False Negative berbahaya |
| **F1-Score**| 2×(P×R) / (P+R)                  | Keseimbangan Precision & Recall           | 0-100% | Balance P & R (umum) |

**Contoh Kasus Penggunaan:**

1. **Spam Email Detection** → Gunakan **Precision**
   - False Positive (email penting masuk spam) lebih berbahaya
   
2. **Cancer Detection** → Gunakan **Recall**
   - False Negative (kanker tidak terdeteksi) lebih berbahaya
   
3. **Document Classification (Kasus Kita)** → Gunakan **F1-Score**
   - Butuh keseimbangan: tidak boleh terlalu banyak salah klasifikasi (FP maupun FN)

**File Implementasi:**

| Komponen           | File/Function                    | Output                     |
| ------------------ | -------------------------------- | -------------------------- |
| Train-Test Split   | `classifier.py: train()`         | X_train, X_test, y_train, y_test |
| Model Prediction   | `classifier.py: evaluate()`      | y_pred array               |
| Confusion Matrix   | `sklearn.metrics.confusion_matrix` | 2×2 matrix                |
| Metrik Calculation | `sklearn.metrics.classification_report` | Dict metrics      |
| Save to DB         | `app.py: /train route`           | Insert ModelMetrics        |
| Visualization      | `templates/evaluation.html`      | Charts + Tables + Heatmap  |

## Struktur Menu

| Menu            | Route         | Fungsi                                                     |
| --------------- | ------------- | ---------------------------------------------------------- |
| **Beranda**     | `/`           | Dashboard dengan statistik data latih dan data uji         |
| **Scraping**    | `/scrape`     | Scraping data dari ejournal.unesa.ac.id + auto-labeling    |
| **Data Latih**  | `/label`      | Lihat data training (hasil scraping dengan auto-label)     |
| **Data Uji**    | `/data-test`  | Lihat history klasifikasi (manual input + file upload)     |
| **Training**    | `/train`      | Latih model KNN dengan data latih (min. 10 data)           |
| **Klasifikasi** | `/classify`   | Klasifikasi abstrak baru (input manual / upload file)      |
| **Evaluasi**    | `/evaluation` | Lihat metrik performa: accuracy, precision, recall, F1     |

## Tips Penggunaan

### Untuk Hasil Klasifikasi Terbaik:

1. **Training Data**: Minimal 50 data per kelas (RPL & TKJ) untuk model yang robust
2. **Quality Data**: Pastikan data training memiliki abstrak yang jelas dan representatif
3. **Upload File**: Gunakan file yang memiliki bagian "ABSTRAK" yang jelas (format Indonesia)
4. **Retraining**: Lakukan training ulang setelah menambah data training baru

### Troubleshooting:

**Model belum di-train**
- Solusi: Lakukan scraping → Training model minimal dengan 10 data

**Ekstraksi abstrak gagal dari PDF/DOCX**
- Pastikan dokumen memiliki header "ABSTRAK" atau "ABSTRACT"
- Atau gunakan copy-paste manual ke input teks

**Accuracy rendah**
- Tambah lebih banyak data training (target: 100+ per kelas)
- Periksa kualitas data: abstrak harus jelas dan berbeda antar kelas

**Data uji tidak tersimpan**
- Pastikan klasifikasi dilakukan setelah model di-train
- Cek database: `ClassificationHistory` table

## Kontribusi

Silakan buka issue atau pull request untuk:
- Bug fixes
- Penambahan fitur baru
- Improvement dokumentasi
- Penambahan keyword untuk auto-labeling

## Lisensi

MIT License

## Pengembang

Dikembangkan sebagai implementasi sistem klasifikasi dokumen menggunakan K-Nearest Neighbor dengan TF-IDF untuk klasifikasi abstrak tugas akhir mahasiswa PTI UNESA.

---

**Repository**: https://github.com/anang2804/Klasifikasi-Abstrak-Tugas-Akhir-Mahasiswa-PTI
