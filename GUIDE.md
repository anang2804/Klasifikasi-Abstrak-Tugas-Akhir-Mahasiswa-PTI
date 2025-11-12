# Panduan Lengkap - Klasifikasi Abstrak Tugas Akhir PTI

## Daftar Isi

1. [Instalasi](#instalasi)
2. [Konfigurasi](#konfigurasi)
3. [Cara Penggunaan](#cara-penggunaan)
4. [Struktur Project](#struktur-project)
5. [API Documentation](#api-documentation)
6. [Troubleshooting](#troubleshooting)

---

## Instalasi

### Persyaratan Sistem

- Python 3.8 atau lebih baru
- pip (Python package manager)
- 2GB RAM minimum
- 500MB disk space

### Langkah Instalasi

#### Windows

```bash
# 1. Clone atau extract project

# 2. Jalankan script setup
run.bat
```

#### Linux/Mac

```bash
# 1. Clone atau extract project

# 2. Berikan permission untuk script
chmod +x run.sh

# 3. Jalankan script setup
./run.sh
```

#### Manual Installation

```bash
# 1. Buat virtual environment
python -m venv venv

# 2. Aktivasi virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_db.py

# 5. Download NLTK data
python -c "import nltk; nltk.download('punkt')"

# 6. Jalankan aplikasi
python app.py
```

---

## Konfigurasi

### Environment Variables

Buat file `.env` berdasarkan `.env.example`:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database.db
```

### Konfigurasi KNN

Edit file `config.py` untuk mengubah parameter:

```python
# KNN Model Settings
KNN_K_VALUE = 5              # Nilai k untuk KNN
TEST_SIZE = 0.2              # Proporsi data test
RANDOM_STATE = 42            # Random seed

# Scraping Settings
START_YEAR = 2020            # Tahun mulai scraping
END_YEAR = 2025              # Tahun akhir scraping
```

---

## Cara Penggunaan

### 1. Scraping Data (dengan Auto-Labeling)

**URL:** `/scrape`

1. Akses halaman scraping
2. Tentukan rentang tahun (default: 2020-2025)
3. Klik "Mulai Scraping"
4. Tunggu proses selesai (beberapa menit)
5. **Otomatis:** Data hasil scraping langsung di-label berdasarkan kata kunci berbobot

**Catatan:**

- Data yang sudah ada tidak akan diduplikasi
- Scraping mengambil dari https://ejournal.unesa.ac.id/index.php/it-edu
- **Auto-labeling otomatis aktif:** Setiap abstrak dianalisis dengan 130+ kata kunci berbobot untuk menentukan label RPL atau TKJ
- Confidence score dihitung berdasarkan total skor kata kunci yang cocok

### 2. Labeling Data (Otomatis)

**URL:** `/label`

**⚡ Auto-Labeling:**

Data hasil scraping **otomatis di-label** menggunakan sistem kata kunci berbobot:

**Kata Kunci RPL** (contoh):

- Pengembangan aplikasi, sistem informasi, database
- Framework (Laravel, React, Flutter, Node.js)
- Testing (black box, white box, usability)
- Machine learning, algoritma, UI/UX
- Dan 70+ kata kunci lainnya dengan bobot 1-3

**Kata Kunci TKJ** (contoh):

- Routing, switching, VLAN, QoS, throughput
- Mikrotik, Cisco, firewall, VPN
- Jaringan (LAN, WAN, wireless), topologi
- IoT network, monitoring jaringan
- Dan 60+ kata kunci lainnya dengan bobot 1-3

**Koreksi Manual (Opsional):**

Jika hasil auto-label kurang akurat, Anda bisa:

1. Buka halaman `/label`
2. Lihat data yang sudah di-label
3. Klik tombol edit untuk mengubah label (RPL ↔ TKJ)

**Target:** Minimal 10 data berlabel untuk training

### 3. Training Model

**URL:** `/train`

1. Pastikan minimal 10 data sudah dilabel (dari hasil scraping + auto-label)
2. Tentukan nilai K (default: 5, disarankan 3-7)
3. Klik "Mulai Training"
4. Tunggu proses selesai
5. Model akan tersimpan otomatis di folder `models/`

**Data Training:**

- **Data Latih:** Semua data yang sudah di-label (hasil scraping + auto-labeling)
- **Data Uji:** Akan diperoleh dari input klasifikasi di menu Klasifikasi

**Proses Training:**

1. Preprocessing teks (case folding, tokenisasi, stopword removal, stemming Sastrawi)
2. Feature extraction (TF-IDF dengan max_features=1000, ngram=(1,2))
3. Split data (80% training, 20% testing untuk validasi internal)
4. Training KNN classifier (dengan cosine distance)
5. Evaluasi dengan test data internal
6. Simpan model (knn_classifier.joblib, tfidf_vectorizer.joblib) dan metrics

### 4. Klasifikasi (Data Uji)

**URL:** `/classify`

**Catatan Penting:** Input yang Anda klasifikasi di sini berfungsi sebagai **Data Uji** untuk model.

#### Opsi 1: Input Teks Manual

1. Paste atau ketik abstrak di text area
2. Klik "Klasifikasi"
3. Lihat hasil prediksi, confidence score, dan kata kunci penting
4. Data ini otomatis tersimpan sebagai data uji

#### Opsi 2: Upload File

1. Pilih tab "Upload File"
2. Upload file TXT, PDF, atau DOCX
3. Klik "Upload dan Klasifikasi"
4. Lihat hasil prediksi

**Fitur Highlight Kata Kunci:**

Sistem menampilkan 20 kata kunci teratas yang paling berpengaruh dalam klasifikasi, dengan highlight di teks asli.

### 5. Evaluasi Model

**URL:** `/evaluation`

Lihat metrik performa model:

- **Accuracy:** Persentase prediksi yang benar
- **Precision:** Ketepatan prediksi positif
- **Recall:** Kemampuan mendeteksi kelas positif
- **F1-Score:** Harmonic mean precision dan recall

Visualisasi tersedia dalam bentuk:

- Bar chart per kelas
- Radar chart perbandingan
- Line chart history training

---

## Struktur Project

```
doc-classifier/
├── app.py                      # Flask application utama
├── config.py                   # Konfigurasi aplikasi
├── models.py                   # Database models (SQLAlchemy)
├── classifier.py               # KNN classifier implementation
├── preprocessing.py            # Text preprocessing (Sastrawi)
├── feature_extraction.py       # TF-IDF feature extraction
├── scraper.py                  # Web scraping module
├── utils.py                    # Utility functions
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows run script
├── run.sh                      # Linux/Mac run script
├── README.md                   # Documentation
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
│
├── templates/                  # HTML templates (Jinja2)
│   ├── base.html              # Base template
│   ├── index.html             # Homepage
│   ├── scrape.html            # Scraping page
│   ├── label.html             # Labeling page
│   ├── train.html             # Training page
│   ├── classify.html          # Classification page
│   ├── evaluation.html        # Evaluation page
│   └── abstract_detail.html   # Abstract detail page
│
├── models/                     # Saved ML models (created at runtime)
│   ├── knn_classifier.joblib
│   ├── tfidf_vectorizer.joblib
│   └── model_metadata.joblib
│
├── uploads/                    # Uploaded files (created at runtime)
└── database.db                 # SQLite database (created at runtime)
```

---

## API Documentation

### REST API Endpoints

#### 1. Label Abstract

```
POST /api/label/<abstract_id>
Content-Type: application/json

Body:
{
  "label": "RPL"  // atau "TKJ"
}

Response:
{
  "success": true,
  "message": "Label saved"
}
```

#### 2. Classify All

```
POST /classify-all
Content-Type: application/json

Response:
{
  "success": true,
  "classified": 50,
  "message": "Successfully classified 50 abstracts"
}
```

#### 3. Get Statistics

```
GET /api/stats

Response:
{
  "total": 100,
  "rpl": 60,
  "tkj": 40,
  "year_distribution": [
    {"year": 2023, "label": "RPL", "count": 30},
    {"year": 2023, "label": "TKJ", "count": 20},
    ...
  ]
}
```

#### 4. Upload File

```
POST /upload
Content-Type: multipart/form-data

Body:
file: [file content]

Response:
{
  "success": true,
  "label": "RPL",
  "confidence": 0.85
}
```

---

## Troubleshooting

### Error: Import "Sastrawi" could not be resolved

**Solusi:**

```bash
pip install Sastrawi
```

### Error: Model belum di-train

**Solusi:**

1. Lakukan labeling data minimal 10 abstrak
2. Kunjungi halaman `/train` dan train model
3. Tunggu hingga proses selesai

### Error: No module named 'flask_sqlalchemy'

**Solusi:**

```bash
pip install Flask-SQLAlchemy
```

### Error: Database tidak ditemukan

**Solusi:**

```bash
python init_db.py
```

### Scraping tidak menemukan data

**Kemungkinan:**

1. Website target sedang down
2. Struktur HTML website berubah
3. Tidak ada artikel di tahun tersebut

**Solusi:**

- Coba tahun yang berbeda
- Cek koneksi internet
- Periksa apakah website bisa diakses manual

### Model accuracy rendah

**Solusi:**

1. Tambah lebih banyak data training
2. Pastikan labeling konsisten dan akurat
3. Coba nilai K yang berbeda (3, 5, 7)
4. Periksa distribusi kelas (balance RPL vs TKJ)

### Memory Error saat training

**Solusi:**

1. Kurangi `max_features` di `feature_extraction.py`
2. Gunakan data yang lebih sedikit
3. Tingkatkan RAM

---

## Pengembangan Lebih Lanjut

### Menambah Kategori Label

Edit file `models.py` dan modifikasi constraint untuk label.

### Mengubah Algoritma

File `classifier.py` dapat dimodifikasi untuk menggunakan algoritma lain (SVM, Naive Bayes, dll).

### Ekstraksi PDF/DOCX

Implementasi ada di `utils.py`, tambahkan library:

- `PyPDF2` untuk PDF
- `python-docx` untuk DOCX

### Custom Stopwords

Edit `preprocessing.py` dan tambahkan kata ke `additional_stopwords`.

---

## Referensi

**Paper:**
Alfian Sukma, Badrus Zaman, Endah Purwanti (2015).
"Klasifikasi Dokumen Temu Kembali Informasi dengan K-Nearest Neighbor"

**Libraries:**

- Flask: https://flask.palletsprojects.com/
- scikit-learn: https://scikit-learn.org/
- Sastrawi: https://github.com/sastrawi/sastrawi

---

## Lisensi

MIT License

## Kontributor

Project dikembangkan untuk keperluan klasifikasi abstrak tugas akhir mahasiswa PTI.
