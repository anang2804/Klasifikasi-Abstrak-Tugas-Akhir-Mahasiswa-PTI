"""
Script untuk auto-labeling data lama yang belum memiliki label
Jalankan sekali untuk update semua data existing
"""
from app import app, db
from models import Abstract
from auto_labeler import auto_label_text

def auto_label_existing_data():
    """
    Auto-label semua data yang belum memiliki label
    """
    with app.app_context():
        # Ambil semua data yang belum punya label (label IS NULL)
        unlabeled_abstracts = Abstract.query.filter(
            Abstract.label.is_(None)
        ).all()
        
        if not unlabeled_abstracts:
            print("✅ Tidak ada data yang perlu di-label. Semua data sudah memiliki label.")
            return
        
        print(f"\n{'='*70}")
        print(f"AUTO-LABELING DATA EXISTING")
        print(f"{'='*70}")
        print(f"\n📊 Ditemukan {len(unlabeled_abstracts)} data yang belum berlabel")
        print(f"🤖 Memulai proses auto-labeling...")
        
        rpl_count = 0
        tkj_count = 0
        
        for i, abstract in enumerate(unlabeled_abstracts, 1):
            # Auto-label menggunakan keyword scoring
            label, confidence = auto_label_text(abstract.abstract_text)
            
            # Update database
            abstract.label = label
            abstract.confidence = confidence
            
            if label == 'RPL':
                rpl_count += 1
            else:
                tkj_count += 1
            
            # Progress indicator setiap 10 data
            if i % 10 == 0 or i == len(unlabeled_abstracts):
                print(f"   Progress: {i}/{len(unlabeled_abstracts)} ({i/len(unlabeled_abstracts)*100:.1f}%)")
        
        # Commit semua perubahan
        try:
            db.session.commit()
            
            print(f"\n{'='*70}")
            print(f"✅ AUTO-LABELING SELESAI!")
            print(f"{'='*70}")
            print(f"\n📈 Hasil:")
            print(f"   Total data di-label: {len(unlabeled_abstracts)}")
            print(f"   RPL: {rpl_count} data ({rpl_count/len(unlabeled_abstracts)*100:.1f}%)")
            print(f"   TKJ: {tkj_count} data ({tkj_count/len(unlabeled_abstracts)*100:.1f}%)")
            
            # Cek distribusi confidence
            high_conf = sum(1 for a in unlabeled_abstracts if a.confidence >= 0.8)
            medium_conf = sum(1 for a in unlabeled_abstracts if 0.6 <= a.confidence < 0.8)
            low_conf = sum(1 for a in unlabeled_abstracts if a.confidence < 0.6)
            
            print(f"\n📊 Distribusi Confidence:")
            print(f"   High (≥0.8):   {high_conf} data ({high_conf/len(unlabeled_abstracts)*100:.1f}%)")
            print(f"   Medium (0.6-0.8): {medium_conf} data ({medium_conf/len(unlabeled_abstracts)*100:.1f}%)")
            print(f"   Low (<0.6):    {low_conf} data ({low_conf/len(unlabeled_abstracts)*100:.1f}%)")
            
            print(f"\n💾 Semua perubahan telah disimpan ke database.")
            print(f"\n🎓 Data siap untuk training model!")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error saat menyimpan ke database: {str(e)}")
            return False
        
        return True


def show_statistics():
    """
    Tampilkan statistik data setelah auto-labeling
    """
    with app.app_context():
        total = Abstract.query.count()
        labeled = Abstract.query.filter(Abstract.label.isnot(None)).count()
        unlabeled = total - labeled
        
        rpl = Abstract.query.filter_by(label='RPL').count()
        tkj = Abstract.query.filter_by(label='TKJ').count()
        
        print(f"\n{'='*70}")
        print(f"STATISTIK DATABASE")
        print(f"{'='*70}")
        print(f"\nTotal Data: {total}")
        print(f"  Berlabel:   {labeled} ({labeled/total*100:.1f}%)")
        print(f"  Belum Label: {unlabeled} ({unlabeled/total*100:.1f}%)")
        print(f"\nDistribusi Label:")
        print(f"  RPL: {rpl} ({rpl/labeled*100:.1f}% dari berlabel)" if labeled > 0 else "  RPL: 0")
        print(f"  TKJ: {tkj} ({tkj/labeled*100:.1f}% dari berlabel)" if labeled > 0 else "  TKJ: 0")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("AUTO-LABEL EXISTING DATA SCRIPT")
    print("="*70)
    
    # Tampilkan statistik sebelum
    print("\n📊 SEBELUM AUTO-LABELING:")
    show_statistics()
    
    # Konfirmasi
    print("\n" + "="*70)
    response = input("\n⚠️  Lanjutkan auto-labeling? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        # Jalankan auto-labeling
        success = auto_label_existing_data()
        
        if success:
            # Tampilkan statistik setelah
            print("\n📊 SETELAH AUTO-LABELING:")
            show_statistics()
    else:
        print("\n❌ Dibatalkan.")
