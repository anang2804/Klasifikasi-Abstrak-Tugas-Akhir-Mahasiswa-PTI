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

### 1. Alur Proses Training Sistem

```
START → Dokumen Testing → Pemberian Label → Text Mining → TF-IDF → Cosine Similarity → KNN → END
                ↑
         Data Training
```

**Mapping ke Menu Website:**

| Tahap                 | Menu Website      | File/Modul              | Keterangan                                   |
| --------------------- | ----------------- | ----------------------- | -------------------------------------------- |
| **Dokumen Testing**   | Menu Beranda      | `templates/index.html`  | Dashboard statistik data latih & uji         |
| **Pemberian Label**   | Menu Scraping     | `auto_labeler.py`       | Auto-label dengan keyword scoring (130+ kw)  |
| **Data Training**     | Menu Data Latih   | `templates/label_data.html` | Data hasil scraping dengan auto-label    |
| **Text Mining**       | Auto di Training  | `preprocessing.py`      | Tokenizing → Stopword Removal → Stemming     |
| **TF-IDF**            | Auto di Training  | `feature_extraction.py` | Raw count TF, IDF smoothing, L2 norm         |
| **Cosine Similarity** | Auto di Training  | `classifier.py`         | Ukur kemiripan dengan cosine similarity      |
| **KNN**               | Menu Training     | `templates/train.html`  | Train & simpan model (k=5, cosine, distance) |
| **Data Testing**      | Menu Data Uji     | `templates/test_data.html` | History klasifikasi (manual + upload)     |

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
START
  ↓
Menggunakan nilai cosine similarity
  ↓
Terdapat kategori mayoritas dalam k-Nearest Neighbor?
  ├─ True → Dokumen yang sudah terklasifikasi → END
  └─ False → Klasifikasi berdasarkan nilai cosine similarity terbesar → (loop back)
```

**Proses Klasifikasi di Menu Klasifikasi:**

1. **Input Abstrak** → User memasukkan teks di `templates/classify.html`

2. **Preprocessing** → Teks diproses dengan Text Mining pipeline

3. **TF-IDF Transform** → Konversi teks hasil preprocessing ke vektor

4. **Hitung Cosine Similarity** → Hitung kemiripan dengan semua data training

   ```
   Cosine Similarity = (A · B) / (||A|| × ||B||)
   ```

5. **Ambil k-Nearest Neighbors** → Ambil 5 dokumen terdekat (k=5)

6. **Voting Mayoritas**:

   - **True** (ada mayoritas): Ambil label mayoritas
     - Contoh: [RPL, RPL, RPL, TKJ, RPL] → **RPL (4/5 = 80%)**
   - **False** (voting seri): Ambil label dari dokumen dengan similarity tertinggi
     - Contoh: [RPL, RPL, TKJ, TKJ] → Pilih yang cosine similarity-nya paling besar

7. **Output Hasil**:
   - Label prediksi (RPL/TKJ)
   - Confidence score (persentase voting)
   - Kata kunci penting (top 20 TF-IDF)
   - Highlight kata penting di teks

**File Implementasi:**

- `classifier.py` → Method `predict_single()`
- Menggunakan `sklearn.neighbors.KNeighborsClassifier` dengan `metric='cosine'`

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
