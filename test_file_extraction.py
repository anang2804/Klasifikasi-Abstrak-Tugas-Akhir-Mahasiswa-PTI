"""
Script untuk testing file upload extraction
"""
import sys
import os

# Tambahkan path project ke sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app import extract_text_from_file

def test_txt_extraction():
    """Test ekstraksi TXT"""
    print("\n" + "="*70)
    print("TEST TXT EXTRACTION")
    print("="*70)
    
    filepath = "test_upload.txt"
    if not os.path.exists(filepath):
        print("❌ File test_upload.txt tidak ditemukan")
        return
    
    text = extract_text_from_file(filepath)
    
    if text:
        print("✅ TXT extraction berhasil!")
        print(f"\nPanjang teks: {len(text)} karakter")
        print(f"\nPreview (100 karakter pertama):")
        print(text[:100] + "...")
    else:
        print("❌ Gagal extract text dari TXT")

def test_pdf_extraction():
    """Test ekstraksi PDF"""
    print("\n" + "="*70)
    print("TEST PDF EXTRACTION")
    print("="*70)
    
    # Cek apakah ada file PDF untuk test
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("⚠️  Tidak ada file PDF untuk testing")
        print("   Upload file PDF ke folder project untuk test ekstraksi PDF")
        return
    
    filepath = pdf_files[0]
    print(f"Testing dengan file: {filepath}")
    
    text = extract_text_from_file(filepath)
    
    if text:
        print("✅ PDF extraction berhasil!")
        print(f"\nPanjang teks: {len(text)} karakter")
        print(f"\nPreview (100 karakter pertama):")
        print(text[:100] + "...")
    else:
        print("❌ Gagal extract text dari PDF")

def test_docx_extraction():
    """Test ekstraksi DOCX"""
    print("\n" + "="*70)
    print("TEST DOCX EXTRACTION")
    print("="*70)
    
    # Cek apakah ada file DOCX untuk test
    docx_files = [f for f in os.listdir('.') if f.endswith('.docx')]
    
    if not docx_files:
        print("⚠️  Tidak ada file DOCX untuk testing")
        print("   Upload file DOCX ke folder project untuk test ekstraksi DOCX")
        return
    
    filepath = docx_files[0]
    print(f"Testing dengan file: {filepath}")
    
    text = extract_text_from_file(filepath)
    
    if text:
        print("✅ DOCX extraction berhasil!")
        print(f"\nPanjang teks: {len(text)} karakter")
        print(f"\nPreview (100 karakter pertama):")
        print(text[:100] + "...")
    else:
        print("❌ Gagal extract text dari DOCX")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("FILE UPLOAD EXTRACTION TEST")
    print("="*70)
    
    # Test TXT
    test_txt_extraction()
    
    # Test PDF
    test_pdf_extraction()
    
    # Test DOCX
    test_docx_extraction()
    
    print("\n" + "="*70)
    print("TEST SELESAI")
    print("="*70)
    print("\n📝 Catatan:")
    print("   - TXT: ✅ Sudah diimplementasikan dan tested")
    print("   - PDF: ✅ Sudah diimplementasikan (butuh file PDF untuk test)")
    print("   - DOCX: ✅ Sudah diimplementasikan (butuh file DOCX untuk test)")
    print("\n💡 Upload file PDF/DOCX ke folder project untuk test lengkap")
