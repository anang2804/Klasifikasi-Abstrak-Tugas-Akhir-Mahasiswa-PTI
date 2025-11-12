# 🎓 Ringkasan Rumus - Menu Klasifikasi (Versi Sederhana)

## 📋 Tahapan Klasifikasi

Ketika Anda input abstrak dan klik **Klasifikasi**, sistem akan:

### 1️⃣ **Text Preprocessing** 🧹

**Tujuan:** Membersihkan dan standarisasi teks

```
Input: "Penelitian ini mengembangkan Aplikasi Mobile Android"
↓
Lowercase: "penelitian ini mengembangkan aplikasi mobile android"
↓
Hapus stopword: "penelitian mengembangkan aplikasi mobile android"
↓
Stemming: "teliti kembang aplikasi mobile android"
```

**Rumus Stemming:** Algoritma Nazief & Adriani (ECS)

- Hapus imbuhan: meng-, di-, -kan, -an, dll
- Contoh: "mengembangkan" → "kembang"

---

### 2️⃣ **TF-IDF Feature Extraction** 🔢

**Tujuan:** Konversi teks jadi angka yang bisa dihitung

#### 📐 Rumus TF (Term Frequency):

```
TF(kata) = Berapa kali kata muncul di dokumen
```

**Contoh:**

- "sistem informasi sistem akademik"
- TF("sistem") = 2

#### 📐 Rumus IDF (Inverse Document Frequency):

```
IDF(kata) = log((Total Dokumen + 1) / (Dokumen yang punya kata + 1)) + 1
```

**Contoh:**

- Total dokumen = 312
- Kata "jaringan" ada di 70 dokumen
- IDF("jaringan") = log((312+1)/(70+1)) + 1 = **1.686** ✅ (kata penting!)

- Kata "sistem" ada di 280 dokumen
- IDF("sistem") = log((312+1)/(280+1)) + 1 = **1.105** (kata umum)

**💡 Artinya:** Kata yang jarang muncul (seperti "jaringan") lebih penting untuk klasifikasi!

#### 📐 Rumus TF-IDF:

```
TF-IDF = TF × IDF
```

**Contoh:**

- Dokumen: "jaringan komputer jaringan wifi"
- TF("jaringan") = 2
- IDF("jaringan") = 1.686
- TF-IDF("jaringan") = 2 × 1.686 = **3.372**

---

### 3️⃣ **Cosine Similarity** 📏

**Tujuan:** Ukur kesamaan antara abstrak Anda dengan 312 data training

#### 📐 Rumus:

```
Similarity = (A · B) / (||A|| × ||B||)

A = Vektor abstrak Anda
B = Vektor data training
A · B = Perkalian dot product
||A|| = Panjang vektor A
```

**Range:** 0 (tidak mirip) sampai 1 (identik)

**Contoh:**

```
Abstrak Anda:    [0.5, 0.3, 0.8, 0.2]
Data Training 1: [0.6, 0.4, 0.7, 0.1]

Dot Product: (0.5×0.6) + (0.3×0.4) + (0.8×0.7) + (0.2×0.1)
           = 0.30 + 0.12 + 0.56 + 0.02 = 1.00

||Anda|| = sqrt(0.5² + 0.3² + 0.8² + 0.2²) = 1.02
||Training1|| = sqrt(0.6² + 0.4² + 0.7² + 0.1²) = 1.06

Similarity = 1.00 / (1.02 × 1.06) = 0.92 = 92% mirip! ✅
```

---

### 4️⃣ **K-Nearest Neighbor (k=5)** 🎯

**Tujuan:** Cari 5 dokumen paling mirip, lalu voting!

#### Contoh Hasil:

```
Abstrak Anda: "aplikasi mobile android java mysql"

Top-5 Tetangga Terdekat:
1. 92% mirip → RPL → "aplikasi android java"
2. 88% mirip → RPL → "mobile apps java"
3. 85% mirip → RPL → "sistem informasi android"
4. 78% mirip → TKJ → "jaringan mobile wifi"
5. 76% mirip → RPL → "web application mysql"

Voting: RPL = 4 suara, TKJ = 1 suara
Hasil: RPL ✅
```

---

### 5️⃣ **Confidence Calculation** 🎲

**Tujuan:** Seberapa yakin sistem dengan prediksinya?

#### 📐 Rumus:

```
Confidence = (Σ Similarity untuk label terpilih) / (Σ Semua similarity)
```

**Contoh:**

```
RPL: 0.92 + 0.88 + 0.85 + 0.76 = 3.41
TKJ: 0.78 = 0.78

Confidence = 3.41 / (3.41 + 0.78) = 0.814 = 81.4% ✅
```

**Interpretasi:**

- ✅ **>80%**: Hasil sangat akurat!
- ⚠️ **60-80%**: Hasil cukup akurat
- ❌ **<60%**: Hasil kurang pasti

---

## 🎨 Visual Pipeline

```
┌─────────────────────────────────────────┐
│  INPUT: "Penelitian ini mengembangkan   │
│  aplikasi mobile Android untuk sistem   │
│  informasi akademik"                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  PREPROCESSING                          │
│  → lowercase, clean, tokenize           │
│  → stopword removal                     │
│  → stemming (Sastrawi)                  │
│                                         │
│  Result: "teliti kembang aplikasi       │
│  mobile android sistem informasi..."    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  TF-IDF VECTORIZATION                   │
│  → TF(kata) = frekuensi                 │
│  → IDF(kata) = log(N/df)                │
│  → TF-IDF = TF × IDF                    │
│                                         │
│  Result: [0.23, 0.19, 0.18, ... 0.00]  │
│          (1000 angka)                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  COSINE SIMILARITY                      │
│  → Hitung dengan 312 data training      │
│  → Similarity = cos(A,B)                │
│                                         │
│  Result: [0.92, 0.88, 0.85, ...]       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  K-NEAREST NEIGHBOR (k=5)               │
│  → Ambil 5 terdekat                     │
│  → Voting berbobot similarity           │
│                                         │
│  Result: RPL (4 votes) vs TKJ (1 vote) │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  OUTPUT                                 │
│  ✅ Label: RPL                          │
│  ✅ Confidence: 81.4%                   │
│  ✅ Top Words: aplikasi, mobile,        │
│     android, sistem, informasi          │
└─────────────────────────────────────────┘
```

---

## 💡 Contoh Sederhana

### Kasus 1: Abstrak RPL (Jelas)

```
Input: "Pengembangan aplikasi web e-commerce menggunakan
        Laravel dan MySQL dengan payment gateway Midtrans"

Top-5 Neighbors:
1. 94% → RPL (laravel, web, aplikasi)
2. 91% → RPL (e-commerce, payment)
3. 89% → RPL (web application, mysql)
4. 87% → RPL (sistem informasi, database)
5. 84% → RPL (aplikasi berbasis web)

Result: RPL - Confidence: 91.2% ✅ TINGGI
```

### Kasus 2: Abstrak TKJ (Jelas)

```
Input: "Implementasi Virtual Private Network (VPN) dengan
        OpenVPN pada jaringan komputer untuk keamanan data"

Top-5 Neighbors:
1. 93% → TKJ (vpn, jaringan, keamanan)
2. 90% → TKJ (openvpn, network security)
3. 86% → TKJ (jaringan komputer, protokol)
4. 82% → TKJ (infrastruktur jaringan)
5. 79% → TKJ (network configuration)

Result: TKJ - Confidence: 86.0% ✅ TINGGI
```

### Kasus 3: Abstrak Ambiguous (Mixed)

```
Input: "Sistem monitoring jaringan berbasis web untuk
        mengelola server dan database"

Top-5 Neighbors:
1. 82% → TKJ (monitoring jaringan, server)
2. 79% → RPL (sistem berbasis web)
3. 76% → TKJ (network management)
4. 74% → RPL (aplikasi web, database)
5. 71% → TKJ (infrastruktur server)

Result: TKJ - Confidence: 65.4% ⚠️ SEDANG
(Ada kata kunci dari kedua kelas)
```

---

## 📚 Parameter yang Digunakan

### TF-IDF:

- `max_features`: 1000 kata
- `ngram_range`: (1,2) - unigram + bigram
- `min_df`: 2 - minimal muncul di 2 dokumen
- `max_df`: 0.8 - maksimal muncul di 80% dokumen
- `norm`: L2 normalization

### KNN:

- `n_neighbors`: 5 tetangga
- `metric`: cosine similarity
- `weights`: distance (voting berbobot)

### Data Training:

- Total: 312 abstrak (242 RPL, 70 TKJ)
- Sumber: ejournal.unesa.ac.id
- Labeling: Otomatis dengan keyword scoring

---

## ❓ FAQ

**Q: Kenapa pakai Cosine Similarity, bukan Euclidean?**
A: Karena fokus ke arah/orientasi teks, bukan panjang dokumen.

**Q: Kenapa k=5?**
A: Berdasarkan eksperimen, k=5 memberikan akurasi terbaik (~85-90%).

**Q: Kenapa confidence kadang rendah?**
A: Abstrak mengandung kata kunci dari kedua kelas (RPL & TKJ).

**Q: Bagaimana cara meningkatkan akurasi?**
A: Tambah data training, terutama untuk kelas minority (TKJ).
