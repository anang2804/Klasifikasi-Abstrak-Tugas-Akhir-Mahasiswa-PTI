# Deploy Full Web App ke Railway

## Langkah-langkah:

### 1. Buat akun Railway
- Kunjungi https://railway.app/
- Sign up dengan GitHub

### 2. Deploy dari GitHub
1. Klik **New Project**
2. Pilih **Deploy from GitHub repo**
3. Pilih repository: `anang2804/Klasifikasi-Abstrak-Tugas-Akhir-Mahasiswa-PTI`
4. Railway akan otomatis detect dan build

### 3. Konfigurasi
Railway akan otomatis menggunakan:
- `Procfile` untuk start command (`gunicorn app:app`)
- `requirements-railway.txt` untuk dependencies

### 4. Set Environment Variables (Optional)
Di Railway dashboard, tambahkan jika diperlukan:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`
- `PORT=5000` (otomatis di-set oleh Railway)

### 5. Deploy
- Railway akan otomatis build dan deploy
- Tunggu ~3-5 menit untuk instalasi scikit-learn
- Dapatkan URL deployment (contoh: `https://your-app.up.railway.app`)
- **Buka URL tersebut di browser** untuk mengakses dashboard web lengkap

### 6. (Optional) Hapus Vercel atau Gunakan untuk API
Karena full app sudah di Railway, Anda bisa:
- **Opsi A**: Hapus deployment Vercel (tidak perlu lagi)
- **Opsi B**: Gunakan Vercel sebagai proxy API dengan set `ML_API_URL` ke Railway URL

## Alternative: Deploy ke Render

### 1. Buat akun Render
- Kunjungi https://render.com/
- Sign up dengan GitHub

### 2. Create Web Service
1. Klik **New +** → **Web Service**
2. Connect repository
3. Konfigurasi:
   - **Name**: doc-classifier-ml
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements-railway.txt`
   - **Start Command**: `gunicorn ml_api:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free

### 3. Deploy
- Klik **Create Web Service**
- Tunggu deployment selesai
- Copy URL deployment

### 4. Update Vercel
Set `ML_API_URL` di Vercel dengan URL dari Render

## Testing Lokal

Test ML API sebelum deploy:

```bash
# Install dependencies
pip install -r requirements-railway.txt

# Run ML API
python ml_api.py

# Test di browser atau curl
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Penelitian tentang jaringan komputer"}'
```

## Catatan Penting

- Model files (`models/*.joblib`) harus sudah ada di repository
- Total ukuran < 500MB untuk Railway free tier
- Railway free tier: 500 hours/month
- Render free tier: Auto-sleep setelah 15 menit idle
