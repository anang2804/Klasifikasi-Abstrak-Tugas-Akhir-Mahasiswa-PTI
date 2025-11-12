# 📐 Rumus Matematis - Menu Klasifikasi

## 🎯 Overview Pipeline Klasifikasi

Ketika user input abstrak di menu **Klasifikasi**, sistem menjalankan pipeline berikut:

```
Input Text → Preprocessing → TF-IDF → KNN → Output (Label + Confidence)
```

---

## 📝 TAHAP 1: TEXT PREPROCESSING

### 1.1 Case Folding

**Rumus:**

```
text_lower = text.toLowerCase()
```

**Contoh:**

```
Input:  "Sistem Informasi Berbasis WEB"
Output: "sistem informasi berbasis web"
```

### 1.2 Cleaning

**Operasi:**

- Hapus URL, email
- Hapus angka
- Hapus tanda baca
- Hapus karakter khusus

**Contoh:**

```
Input:  "aplikasi mobile (android) v2.0"
Output: "aplikasi mobile android"
```

### 1.3 Tokenisasi

**Rumus:**

```
tokens = text.split(' ')
tokens = [t for t in tokens if len(t) >= 3]
```

**Contoh:**

```
Input:  "sistem informasi akademik"
Output: ["sistem", "informasi", "akademik"]
```

### 1.4 Stopword Removal

**Rumus:**

```
tokens_filtered = [t for t in tokens if t not in stopwords]
```

**Stopwords:** dan, atau, yang, di, ke, dari, untuk, dengan, pada, adalah, dll (total ~750 kata)

**Contoh:**

```
Input:  ["sistem", "informasi", "untuk", "akademik"]
Output: ["sistem", "informasi", "akademik"]
```

### 1.5 Stemming (Sastrawi)

**Algoritma:** Nazief & Adriani (ECS Stemmer)

**Aturan:**

1. Hapus Particle (kah, lah, pun)
2. Hapus Possessive Pronoun (ku, mu, nya)
3. Hapus Derivation Suffixes (i, kan, an)
4. Hapus Derivation Prefixes (meng, di, ter, ber, pe)
5. Recoding (bentuk ulang/reduplikasi)

**Contoh:**

```
"mengembangkan" → "kembang"
"pengelolaan"   → "kelola"
"digunakan"     → "guna"
"pembelajaran"  → "ajar"
```

**Hasil Akhir Preprocessing:**

```
Input:  "Penelitian ini mengembangkan sistem informasi untuk pengelolaan data"
Output: "teliti kembang sistem informasi kelola data"
```

---

## 🔢 TAHAP 2: TF-IDF FEATURE EXTRACTION

### 2.1 Term Frequency (TF)

**Rumus:**

```
TF(d, t) = f(d, t)
```

Dimana:

- `d` = dokumen
- `t` = term (kata)
- `f(d, t)` = frekuensi kemunculan term t dalam dokumen d (raw count)

**Contoh:**

```
Dokumen: "sistem informasi sistem akademik"
TF("sistem") = 2
TF("informasi") = 1
TF("akademik") = 1
```

### 2.2 Inverse Document Frequency (IDF)

**Rumus:**

```
IDF(t) = log((N + 1) / (df(t) + 1)) + 1
```

Dimana:

- `N` = total jumlah dokumen dalam corpus (312)
- `df(t)` = jumlah dokumen yang mengandung term t
- `+1` = smoothing untuk hindari division by zero

**Contoh:**

```
N = 312 dokumen
df("sistem") = 280 dokumen (kata umum)
df("jaringan") = 70 dokumen (kata spesifik TKJ)

IDF("sistem")   = log((312+1)/(280+1)) + 1 = 1.105
IDF("jaringan") = log((312+1)/(70+1)) + 1  = 1.686
```

**Interpretasi:**

- IDF tinggi → kata jarang muncul → lebih diskriminatif
- IDF rendah → kata sering muncul → kurang informatif

### 2.3 TF-IDF Score

**Rumus:**

```
TF-IDF(d, t) = TF(d, t) × IDF(t)
```

**Contoh:**

```
Dokumen RPL: "sistem informasi aplikasi web sistem database"

TF("sistem") = 2
IDF("sistem") = 1.105
TF-IDF("sistem") = 2 × 1.105 = 2.210

TF("web") = 1
IDF("web") = 1.450
TF-IDF("web") = 1 × 1.450 = 1.450
```

### 2.4 Normalisasi L2

**Rumus:**

```
v_normalized = v / ||v||₂

||v||₂ = sqrt(Σ vᵢ²)
```

**Tujuan:** Normalisasi panjang dokumen agar tidak bias pada dokumen panjang

**Contoh:**

```
Vector: [2.210, 1.450, 1.800]
Norm: sqrt(2.210² + 1.450² + 1.800²) = 3.315

Normalized: [2.210/3.315, 1.450/3.315, 1.800/3.315]
          = [0.667, 0.437, 0.543]
```

### 2.5 Matrix Representation

**Struktur:**

```
         kata₁  kata₂  kata₃  ...  kataₙ
dok₁   [ 0.45   0.32   0.00  ...  0.12 ]
dok₂   [ 0.00   0.67   0.55  ...  0.21 ]
...
dokₘ   [ 0.28   0.00   0.44  ...  0.39 ]
```

**Dimensi:**

- Baris = Dokumen (1 untuk query, 312 untuk training)
- Kolom = Fitur/kata (max 1000 kata, bigram included)
- Nilai = TF-IDF score (normalized)

**Parameter TF-IDF Vectorizer:**

```python
max_features = 1000      # Max 1000 kata paling penting
ngram_range = (1, 2)     # Unigram + Bigram
min_df = 2               # Min muncul di 2 dokumen
max_df = 0.8             # Max muncul di 80% dokumen
sublinear_tf = False     # TF raw count (bukan log)
use_idf = True           # Gunakan IDF
smooth_idf = True        # IDF smoothing (+1)
norm = 'l2'              # L2 normalization
```

---

## 🎯 TAHAP 3: K-NEAREST NEIGHBOR (KNN)

### 3.1 Cosine Similarity

**Rumus:**

```
cos(x, y) = (x · y) / (||x||₂ × ||y||₂)

x · y = Σ(xᵢ × yᵢ)  -- dot product
```

**Range:** 0 (tidak mirip) hingga 1 (identik)

**Contoh:**

```
Query:     [0.5, 0.3, 0.0, 0.8]
Training1: [0.6, 0.4, 0.1, 0.7]

Dot product: (0.5×0.6) + (0.3×0.4) + (0.0×0.1) + (0.8×0.7)
           = 0.30 + 0.12 + 0.00 + 0.56
           = 0.98

||Query|| = sqrt(0.5² + 0.3² + 0.0² + 0.8²) = 0.989
||Training1|| = sqrt(0.6² + 0.4² + 0.1² + 0.7²) = 1.022

Cosine Similarity = 0.98 / (0.989 × 1.022) = 0.969
```

**Interpretasi:**

- 0.969 = Sangat mirip! (>95%)
- 0.500 = Cukup mirip (50%)
- 0.100 = Tidak mirip (<10%)

### 3.2 Distance Metric

**Cosine Distance:**

```
distance(x, y) = 1 - cos(x, y)
```

**Contoh:**

```
Cosine Similarity = 0.969
Cosine Distance = 1 - 0.969 = 0.031 (sangat dekat!)
```

### 3.3 Finding K-Nearest Neighbors

**Algoritma:**

```
1. Hitung cosine similarity query dengan SEMUA 312 training data
2. Sort berdasarkan similarity (descending)
3. Ambil top-k tetangga terdekat (k=5)
4. Voting berdasarkan label mayoritas
```

**Contoh dengan k=5:**

```
Query: "aplikasi mobile android java mysql"

Top-5 Nearest:
1. Doc_15  - RPL - similarity: 0.92 - "aplikasi android java database"
2. Doc_89  - RPL - similarity: 0.88 - "mobile apps java firebase"
3. Doc_142 - RPL - similarity: 0.85 - "sistem informasi android"
4. Doc_201 - TKJ - similarity: 0.78 - "jaringan mobile wifi"
5. Doc_55  - RPL - similarity: 0.76 - "web application php mysql"

Voting: RPL=4, TKJ=1
Hasil: RPL
```

### 3.4 Weighted Voting

**Rumus:**

```
weight(i) = similarity(query, neighbor_i)

score(class) = Σ weight(i) for all neighbors with label=class
```

**Contoh:**

```
Neighbor 1: RPL, similarity=0.92 → weight=0.92
Neighbor 2: RPL, similarity=0.88 → weight=0.88
Neighbor 3: RPL, similarity=0.85 → weight=0.85
Neighbor 4: TKJ, similarity=0.78 → weight=0.78
Neighbor 5: RPL, similarity=0.76 → weight=0.76

Score RPL = 0.92 + 0.88 + 0.85 + 0.76 = 3.41
Score TKJ = 0.78 = 0.78

Predicted: RPL
Confidence: 3.41 / (3.41 + 0.78) = 0.814 = 81.4%
```

**Parameter KNN:**

```python
n_neighbors = 5          # k=5 tetangga terdekat
metric = 'cosine'        # Cosine similarity
weights = 'distance'     # Weighted voting (bukan uniform)
```

---

## 📊 TAHAP 4: CONFIDENCE CALCULATION

### 4.1 Probability Estimation

**Rumus (Weighted KNN):**

```
P(class_c | query) = Σ weight(i) / Σ all_weights

Dimana weight(i) untuk neighbors dengan label = class_c
```

**Contoh:**

```
Dari 5 neighbors:
- 4 neighbors RPL dengan weights: [0.92, 0.88, 0.85, 0.76] = sum: 3.41
- 1 neighbor TKJ dengan weight: 0.78

P(RPL | query) = 3.41 / (3.41 + 0.78) = 0.814 = 81.4%
P(TKJ | query) = 0.78 / (3.41 + 0.78) = 0.186 = 18.6%

Confidence = max(P) = 81.4%
```

### 4.2 Interpretasi Confidence

```
Confidence >= 80%  → TINGGI   (hasil sangat akurat)
60% <= Confidence < 80%  → SEDANG  (hasil cukup akurat)
Confidence < 60%   → RENDAH  (hasil kurang pasti)
```

---

## 🔍 TAHAP 5: IMPORTANT WORDS IDENTIFICATION

### 5.1 Top-N TF-IDF Words

**Rumus:**

```
top_words = argsort(TF-IDF_scores)[-n:][::-1]
```

**Contoh:**

```
Query TF-IDF scores:
"aplikasi": 0.245
"mobile":   0.198
"android":  0.187
"java":     0.156
"mysql":    0.134
...

Top-5: aplikasi, mobile, android, java, mysql
```

### 5.2 Word Highlighting

**Mapping:**

```
Stemmed word → Original variations in text

"kembang" → ["mengembangkan", "pengembangan", "dikembangkan"]
"kelola"  → ["pengelolaan", "mengelola", "dikelola"]
```

---

## 📈 SUMMARY: Complete Mathematical Pipeline

```
1. INPUT TEXT
   ↓
2. PREPROCESSING
   text → lowercase → clean → tokenize → stopwords → stem
   ↓
3. TF-IDF VECTORIZATION
   TF(d,t) = f(d,t)
   IDF(t) = log((N+1)/(df(t)+1)) + 1
   TF-IDF(d,t) = TF(d,t) × IDF(t)
   Normalize: v / ||v||₂
   ↓
4. COSINE SIMILARITY
   cos(x,y) = (x·y) / (||x|| × ||y||)
   Compute with ALL 312 training vectors
   ↓
5. K-NEAREST NEIGHBORS
   Sort by similarity
   Take top-k=5 neighbors
   ↓
6. WEIGHTED VOTING
   Score(class) = Σ similarity(i) for label=class
   Confidence = max(Score) / Σ all_scores
   ↓
7. OUTPUT
   Predicted Label: RPL/TKJ
   Confidence: 0-100%
   Important Words: Top-N TF-IDF terms
```

---

## 🧪 Contoh Real Case

### Input:

```
"Penelitian ini mengembangkan aplikasi mobile berbasis Android
untuk sistem informasi akademik menggunakan Java dan MySQL"
```

### Step-by-Step:

**1. Preprocessing:**

```
Original: "Penelitian ini mengembangkan aplikasi mobile..."
Cleaned:  "penelitian mengembangkan aplikasi mobile android sistem informasi..."
Tokens:   ["penelitian", "mengembangkan", "aplikasi", "mobile", ...]
Stemmed:  ["teliti", "kembang", "aplikasi", "mobile", "android", "sistem", ...]
```

**2. TF-IDF:**

```
Vector: [0.00, 0.23, 0.19, 0.18, 0.16, ..., 0.00]
         (1000 dimensions)
```

**3. Similarity (Top-5):**

```
Doc_15:  0.89 - RPL - "aplikasi android java"
Doc_142: 0.87 - RPL - "sistem informasi mobile"
Doc_89:  0.84 - RPL - "mobile apps database"
Doc_55:  0.81 - RPL - "aplikasi web mysql"
Doc_201: 0.73 - TKJ - "jaringan mobile"
```

**4. Voting:**

```
RPL: 0.89 + 0.87 + 0.84 + 0.81 = 3.41
TKJ: 0.73 = 0.73

Confidence: 3.41/(3.41+0.73) = 82.3%
```

**5. Output:**

```
✅ Predicted Label: RPL
✅ Confidence: 82.3%
✅ Top Words: aplikasi, mobile, android, sistem, informasi
```

---

## 📚 Referensi Rumus

1. **TF-IDF:**
   - Salton, G., & Buckley, C. (1988). "Term-weighting approaches in automatic text retrieval"
2. **Cosine Similarity:**
   - Singhal, A. (2001). "Modern Information Retrieval: A Brief Overview"
3. **K-Nearest Neighbor:**
   - Cover, T., & Hart, P. (1967). "Nearest neighbor pattern classification"
4. **Stemming (Sastrawi):**

   - Nazief, B., & Adriani, M. (1996). "Confix Stripping: Approach to Stemming Algorithm for Bahasa Indonesia"

5. **Jurnal Referensi Utama:**
   - Alfian Sukma, Badrus Zaman, Endah Purwanti (2015).
     "Klasifikasi Dokumen Temu Kembali Informasi dengan K-Nearest Neighbor"
