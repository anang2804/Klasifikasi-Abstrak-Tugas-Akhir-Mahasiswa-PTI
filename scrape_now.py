"""
Script untuk scraping langsung dari terminal
"""
from app import app
from scraper import scrape_and_save
from config import Config

def main():
    with app.app_context():
        print("=" * 70)
        print("MULAI SCRAPING DATA")
        print("=" * 70)
        print(f"URL        : {Config.BASE_URL}")
        print(f"Tahun      : {Config.START_YEAR} - {Config.END_YEAR}")
        print(f"\nProses scraping dimulai...")
        print("-" * 70)
        
        result = scrape_and_save(
            Config.BASE_URL,
            Config.START_YEAR,
            Config.END_YEAR
        )
        
        print("\n" + "=" * 70)
        print("HASIL SCRAPING")
        print("=" * 70)
        print(f"Total Scraped : {result['total_scraped']} artikel")
        print(f"Total Saved   : {result['total_saved']} artikel baru")
        print(f"Message       : {result['message']}")
        print("=" * 70)
        print("\n✅ Scraping selesai! Jalankan 'python view_db.py' untuk melihat hasilnya.")

if __name__ == '__main__':
    main()
