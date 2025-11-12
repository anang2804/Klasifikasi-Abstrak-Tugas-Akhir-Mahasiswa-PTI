# Implementasi TF-IDF dalam Kode

## Rumus yang Digunakan

### 1. Term Frequency (TF)

```
TF(d,t) = f(d,t)
```

**Keterangan:**

- `f(d,t)` = kemunculan kata `t` dalam dokumen `d` (raw count)

### 2. Inverse Document Frequency (IDF)

```
IDF(t) = log(N/df(t))
```

**Keterangan:**

- `N` = jumlah total dokumen
- `df(t)` = jumlah dokumen yang memiliki kata `t`

### 3. TF-IDF

```
TFIDF = TF(d,t) × IDF(t)
```

### 4. Cosine Similarity

```
cos(x,y) = (x·y) / (||x|| ||y||)
```

**Keterangan:**

- `x·y = Σ(x_k × y_k)` = dot product
- `||x|| = sqrt(Σ x_k²)` = panjang vektor x
- `||y|| = sqrt(Σ y_k²)` = panjang vektor y

## Implementasi dalam Kode

### File: `feature_extraction.py`

#### Class FeatureExtractor

```python
self.vectorizer = TfidfVectorizer(
    max_features=1000,        # Maksimal 1000 fitur teratas
    ngram_range=(1, 2),       # Unigram dan bigram
    min_df=2,                 # Minimal muncul di 2 dokumen
    max_df=0.8,               # Maksimal muncul di 80% dokumen
    sublinear_tf=False,       # TF(d,t) = f(d,t) - raw count
    use_idf=True,             # Gunakan IDF: log(N/df(t))
    smooth_idf=True,          # IDF = log((N+1)/(df(t)+1)) + 1
    norm='l2'                 # Normalisasi L2 untuk cosine similarity
)
```

**Parameter Penting:**

- `sublinear_tf=False` → Menggunakan raw count `f(d,t)` sesuai rumus (2.1)
- `use_idf=True` → Menggunakan IDF sesuai rumus (2.2)
- `smooth_idf=True` → Mencegah divide-by-zero dengan smoothing
- `norm='l2'` → Normalisasi L2 diperlukan untuk cosine similarity

#### Class SimilarityCalculator

```python
def cosine_similarity_pair(vector1, vector2):
    """
    Menghitung cosine similarity antara dua vektor
    Implementasi: cos(x,y) = (x·y) / (||x|| ||y||)
    """
    return cosine_similarity(vector1, vector2)[0][0]
```

### File: `classifier.py`

#### KNN Classifier

```python
self.classifier = KNeighborsClassifier(
    n_neighbors=k,           # Jumlah tetangga (default: 5)
    metric='cosine',         # Menggunakan cosine distance
    weights='distance'       # Bobot berdasarkan jarak
)
```

## Pipeline Lengkap

1. **Preprocessing** (`preprocessing.py`)

   - Lowercase
   - Hapus URL, email, angka, tanda baca
   - Tokenisasi
   - Stopword removal
   - Stemming (Sastrawi)

2. **Feature Extraction** (`feature_extraction.py`)

   - Input: teks yang sudah dipreprocess
   - Proses: Hitung TF-IDF untuk setiap kata
   - Output: Matriks TF-IDF (sparse matrix)

3. **Klasifikasi** (`classifier.py`)
   - Input: Vektor TF-IDF dokumen baru
   - Proses:
     1. Hitung cosine similarity dengan semua dokumen training
     2. Ambil k tetangga terdekat (k=5)
     3. Voting mayoritas dengan bobot jarak
   - Output: Label prediksi (RPL/TKJ) dan confidence score

## Contoh Perhitungan

### Dokumen Training:

- D1 (RPL): "sistem informasi akademik"
- D2 (TKJ): "jaringan komputer server"

### Dokumen Test:

- D_test: "sistem jaringan"

### Langkah 1: Preprocessing

- D1 → ["sistem", "inform", "akadem"]
- D2 → ["jaring", "komput", "serv"]
- D_test → ["sistem", "jaring"]

### Langkah 2: TF-IDF

```
Vocabulary: ["sistem", "inform", "akadem", "jaring", "komput", "serv"]

TF untuk D_test:
- sistem: 1
- jaring: 1
- (lainnya: 0)

IDF:
- sistem: log(2/1) = 0.693
- jaring: log(2/1) = 0.693

TF-IDF D_test:
- sistem: 1 × 0.693 = 0.693
- jaring: 1 × 0.693 = 0.693
```

### Langkah 3: Cosine Similarity

```
cos(D_test, D1) = dot(D_test, D1) / (||D_test|| × ||D1||)
cos(D_test, D2) = dot(D_test, D2) / (||D_test|| × ||D2||)
```

### Langkah 4: KNN

- Ambil k=5 tetangga terdekat (similarity tertinggi)
- Voting mayoritas berdasarkan label
- Hasil: Prediksi label dan confidence score

## Verifikasi Implementasi

✅ TF menggunakan raw count (sublinear_tf=False)
✅ IDF menggunakan log(N/df(t))
✅ Cosine similarity untuk jarak
✅ KNN dengan k=5 dan voting berdasarkan jarak

## Hasil Training Terbaru

```
Accuracy : 78.57%
Precision: 78.46%
Recall   : 78.46%
F1 Score : 78.46%

Confusion Matrix:
            Predicted
            RPL    TKJ
Actual RPL   12      3
       TKJ    3     10
```

Model tersimpan di: `models/knn_classifier.joblib` dan `models/tfidf_vectorizer.joblib`
