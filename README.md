# Klasifikasi Abstrak Tugas Akhir Mahasiswa PTI Berdasarkan Bidang Keahlian Menggunakan K-Nearest Neighbor (KNN)

## Deskripsi

Website ini mengklasifikasikan abstrak tugas akhir mahasiswa Program Studi PTI ke dalam dua kategori utama:

- **Rekayasa Perangkat Lunak (RPL)**
- **Teknik Komputer dan Jaringan (TKJ)**

## Fitur Utama

- ✅ Web scraping otomatis dari ejournal.unesa.ac.id (2020-2025)
- ✅ **Auto-label data hasil scraping** menggunakan model yang sudah di-train
- ✅ **Auto-label semua data existing** yang belum berlabel dengan satu klik
- ✅ Preprocessing teks Bahasa Indonesia (tokenisasi, stopword removal, stemming)
- ✅ Feature extraction menggunakan TF-IDF
- ✅ Klasifikasi dokumen menggunakan algoritma K-Nearest Neighbor (KNN)
- ✅ Evaluasi model dengan metrik Precision, Recall, dan F1-Score
- ✅ Visualisasi hasil klasifikasi dalam bentuk grafik
- ✅ Upload dan klasifikasi abstrak baru

## Teknologi

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn
- **Text Processing**: Sastrawi, NLTK
- **Scraping**: BeautifulSoup
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap, Chart.js

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
- Data akan disimpan otomatis ke database tanpa label
- Setelah scraping, akan diarahkan ke halaman Label Data Training

### 2. Labeling Data

- Akses halaman `/label` untuk memberikan label pada data
- **Opsi 1:** Label manual satu-per-satu (untuk data training berkualitas)
- **Opsi 2:** Klik tombol **"Auto-Label Semua"** untuk otomatis label semua data (jika model sudah di-train)
- Minimal 10 data berlabel diperlukan untuk training

### 3. Training Model

- Akses halaman `/train` untuk melatih model KNN
- Model akan disimpan dan siap digunakan untuk klasifikasi
- Setelah training, auto-label akan aktif di scraping

### 4. Klasifikasi

- Halaman utama menampilkan hasil klasifikasi semua abstrak
- Gunakan fitur upload untuk mengklasifikasi abstrak baru
- Data dengan label akan muncul di visualisasi dan statistik

### 5. Evaluasi

- Lihat hasil evaluasi model di halaman `/evaluation`
- Grafik distribusi dan metrik performa ditampilkan

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

| Tahap                 | Menu Website     | File/Modul              | Keterangan                          |
| --------------------- | ---------------- | ----------------------- | ----------------------------------- |
| **Dokumen Testing**   | Menu Beranda     | `templates/index.html`  | Menampilkan semua dokumen/abstrak   |
| **Pemberian Label**   | Menu Label Data  | `templates/label.html`  | User memberi label manual (RPL/TKJ) |
| **Text Mining**       | Auto di Training | `preprocessing.py`      | Tokenizing → Filtering → Stemming   |
| **TF-IDF**            | Auto di Training | `feature_extraction.py` | Konversi teks ke vektor numerik     |
| **Cosine Similarity** | Auto di Training | `classifier.py`         | Ukur kemiripan antar dokumen        |
| **KNN**               | Menu Training    | `templates/train.html`  | Simpan model KNN (k=5)              |
| **Data Training**     | Menu Label Data  | Query database          | Data dengan label manual saja       |

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

## Metode KNN

1. **Text Preprocessing**: Tokenisasi, Stopword Removal, Stemming (Sastrawi)
2. **Feature Extraction**: TF-IDF Weighting (max_features=1000)
3. **Similarity Measure**: Cosine Similarity
4. **Classification**: Voting berdasarkan k=5 tetangga terdekat
5. **Evaluation**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix

## Struktur Menu

| Menu            | Route         | Fungsi                                   |
| --------------- | ------------- | ---------------------------------------- |
| **Beranda**     | `/`           | Tampilkan semua abstrak dengan statistik |
| **Scraping**    | `/scrape`     | Scraping data dari ejournal.unesa.ac.id  |
| **Label Data**  | `/label`      | Labeling manual abstrak (untuk training) |
| **Training**    | `/train`      | Latih model KNN dengan data berlabel     |
| **Klasifikasi** | `/classify`   | Klasifikasi abstrak baru real-time       |
| **Evaluasi**    | `/evaluation` | Lihat metrik performa model              |

## Lisensi

MIT License
