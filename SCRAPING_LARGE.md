# Scraping Data Besar

Untuk scraping range tahun yang besar (> 2 tahun), gunakan salah satu cara berikut:

## Cara 1: Scraping Bertahap Manual di Web

Scrape secara manual per 2 tahun:
1. Scrape 2017-2018
2. Scrape 2019-2020
3. Scrape 2021-2022
4. Scrape 2023-2024
5. Scrape 2025

## Cara 2: Gunakan Script CLI (Lokal)

```bash
# Di komputer lokal
python scrape_large.py 2017 2025
```

Script akan otomatis split menjadi batch dan scrape semua data.

## Cara 3: Railway CLI (One-time Job)

Jika sudah deploy di Railway, jalankan one-time command:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Run scraping
railway run python scrape_large.py 2017 2025
```

## Cara 4: Pre-populate dari Database Backup

Jika ada database backup dengan data lengkap:
1. Export database lokal yang sudah ada data
2. Import ke Railway database

## Rekomendasi

Untuk deployment pertama dengan data besar:
- **Gunakan Cara 2 (Lokal)**: Scrape di komputer lokal, lalu database otomatis sync ke Railway
- **Gunakan Cara 1 (Manual)**: Paling aman, tidak ada timeout issue
