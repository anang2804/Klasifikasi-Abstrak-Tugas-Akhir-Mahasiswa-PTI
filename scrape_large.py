#!/usr/bin/env python
"""
Script untuk scraping data dalam jumlah besar
Jalankan: python scrape_large.py START_YEAR END_YEAR

Contoh: python scrape_large.py 2017 2025
"""
import sys
import os
from app import app, db
from scraper import scrape_and_save
from config import Config

def scrape_large_range(start_year, end_year):
    """Scrape data untuk range tahun yang besar dengan batching otomatis"""
    
    with app.app_context():
        print(f"\n{'='*60}")
        print(f"SCRAPING DATA: {start_year} - {end_year}")
        print(f"{'='*60}\n")
        
        total_saved = 0
        total_rpl = 0
        total_tkj = 0
        
        # Scrape per batch 2 tahun
        current_year = start_year
        batch_num = 1
        
        while current_year <= end_year:
            batch_end = min(current_year + 1, end_year)
            
            print(f"\n[Batch {batch_num}] Scraping: {current_year}-{batch_end}")
            print(f"{'-'*60}")
            
            try:
                result = scrape_and_save(
                    Config.BASE_URL,
                    current_year,
                    batch_end,
                    auto_label=True
                )
                
                batch_saved = result.get('total_saved', 0)
                batch_rpl = result.get('rpl_count', 0)
                batch_tkj = result.get('tkj_count', 0)
                
                total_saved += batch_saved
                total_rpl += batch_rpl
                total_tkj += batch_tkj
                
                print(f"✅ Batch selesai: {batch_saved} data (RPL: {batch_rpl}, TKJ: {batch_tkj})")
                
            except Exception as e:
                print(f"❌ Error pada batch {current_year}-{batch_end}: {str(e)}")
            
            current_year = batch_end + 1
            batch_num += 1
        
        print(f"\n{'='*60}")
        print(f"SCRAPING SELESAI!")
        print(f"Total: {total_saved} data")
        print(f"RPL: {total_rpl} | TKJ: {total_tkj}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python scrape_large.py START_YEAR END_YEAR")
        print("Example: python scrape_large.py 2017 2025")
        sys.exit(1)
    
    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        
        if start > end:
            print("Error: START_YEAR harus lebih kecil atau sama dengan END_YEAR")
            sys.exit(1)
        
        scrape_large_range(start, end)
        
    except ValueError:
        print("Error: START_YEAR dan END_YEAR harus berupa angka")
        sys.exit(1)
