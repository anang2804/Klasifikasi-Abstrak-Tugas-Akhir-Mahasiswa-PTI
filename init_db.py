"""
Script untuk inisialisasi database dan data sample
"""
from app import app, db
from models import Abstract


def init_database():
    """Initialize database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")


def add_sample_data():
    """Add sample data untuk testing (opsional)"""
    with app.app_context():
        # Cek apakah sudah ada data
        if Abstract.query.count() > 0:
            print("Database already contains data. Skipping sample data insertion.")
            return
        
        sample_abstracts = [
            {
                'title': 'Pengembangan Aplikasi Mobile Berbasis Android untuk Sistem Informasi Akademik',
                'author': 'John Doe',
                'year': 2023,
                'abstract_text': 'Penelitian ini bertujuan untuk mengembangkan aplikasi mobile berbasis Android yang dapat membantu mahasiswa dalam mengakses informasi akademik. Aplikasi ini dikembangkan menggunakan Java dan Android Studio dengan database MySQL. Fitur yang tersedia meliputi jadwal kuliah, nilai, dan informasi dosen.',
                'label': 'RPL'
            },
            {
                'title': 'Implementasi Jaringan Virtual Private Network (VPN) untuk Keamanan Data',
                'author': 'Jane Smith',
                'year': 2023,
                'abstract_text': 'Penelitian ini membahas implementasi VPN untuk meningkatkan keamanan data dalam komunikasi jaringan. Menggunakan protokol OpenVPN dan konfigurasi firewall untuk melindungi data yang dikirimkan melalui internet. Hasil pengujian menunjukkan peningkatan keamanan signifikan.',
                'label': 'TKJ'
            },
            {
                'title': 'Sistem Pakar Diagnosa Penyakit Menggunakan Metode Forward Chaining',
                'author': 'Ahmad Rizki',
                'year': 2024,
                'abstract_text': 'Sistem pakar ini dikembangkan untuk membantu mendiagnosa penyakit berdasarkan gejala yang dialami pasien. Menggunakan metode forward chaining dan basis pengetahuan dari dokter ahli. Sistem dibuat dengan PHP dan MySQL dengan antarmuka web yang user-friendly.',
                'label': 'RPL'
            },
        ]
        
        print("Adding sample data...")
        for data in sample_abstracts:
            abstract = Abstract(**data)
            abstract.is_training_data = True
            db.session.add(abstract)
        
        db.session.commit()
        print(f"Added {len(sample_abstracts)} sample abstracts successfully!")


if __name__ == '__main__':
    init_database()
    
    # Uncomment untuk menambah sample data
    # add_sample_data()
    
    print("\nDatabase initialization complete!")
    print("You can now run the application with: python app.py")
