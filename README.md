# ATS - Applicant Tracking System

🎯 **Sistem Pelacakan Pelamar Kerja dengan Algoritma String Matching**

## 📖 Deskripsi

ATS (Applicant Tracking System) adalah aplikasi desktop yang dikembangkan untuk membantu perusahaan dalam mengelola dan mencari CV pelamar kerja menggunakan algoritma string matching yang efisien.

### ✨ Fitur Utama

- 🔍 **Pencarian CV Cerdas** - Menggunakan algoritma KMP dan Boyer-Moore
- 📊 **Fuzzy Matching** - Pencarian dengan toleransi kesalahan menggunakan Levenshtein Distance
- 🗄️ **Database Integration** - Penyimpanan data terstruktur dengan MariaDB/MySQL
- 🖥️ **GUI User-Friendly** - Interface desktop yang mudah digunakan
- 📈 **Analisis Performa** - Perbandingan waktu eksekusi algoritma
- 📝 **Ekstraksi PDF** - Otomatis mengekstrak teks dari file CV PDF

### 🛠️ Teknologi yang Digunakan

- **Python 3.11+** - Bahasa pemrograman utama
- **Tkinter** - GUI framework
- **MariaDB/MySQL** - Database sistem
- **PyMuPDF** - PDF text extraction
- **PyMySQL** - Database connector

## 🚀 Instalasi dan Setup

### Prerequisites

1. **Python 3.11 atau lebih baru**
2. **MariaDB 11.8 atau MySQL 8.0+**
3. **Git** (opsional)

### Langkah Instalasi

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd Tubes3_atsTracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   - Pastikan MariaDB/MySQL berjalan
   - Buat database: `CREATE DATABASE ats_db;`
   - Import schema: 
     ```bash
     mysql -u root -p ats_db < database/database_schema.sql
     ```

4. **Konfigurasi database**
   - Edit `config.py` sesuai pengaturan database Anda
   - Pastikan username, password, dan host sudah benar

5. **Seed data sample (opsional)**
   ```bash
   python database/seeding_db.py
   ```

## 📁 Struktur Project

```
Tubes3_atsTracker/
├── algorithms/           # Implementasi algoritma string matching
│   ├── KMP.py           # Knuth-Morris-Pratt algorithm
│   ├── BM.py            # Boyer-Moore algorithm
│   └── levenshtein.py   # Levenshtein Distance
├── database/            # Database setup dan koneksi
│   ├── database.py      # Database connection class
│   ├── database_schema.sql  # Schema database
│   └── seeding_db.py    # Data seeding script
├── data/               # Sample CV files
│   ├── Designer/       # CV untuk posisi Designer
│   ├── Engineer/       # CV untuk posisi Engineer
│   ├── HR/            # CV untuk posisi HR
│   ├── Marketing/     # CV untuk posisi Marketing
│   └── Sales/         # CV untuk posisi Sales
├── gui/               # Graphical User Interface
│   └── main_gui.py    # Main GUI application
├── src/               # Core application logic
│   ├── cv_matcher.py  # CV matching engine
│   └── ekstrak_regex.py  # PDF text extraction
├── scripts/           # Utility scripts
├── tests/             # Test files
├── config.py          # Configuration file
├── main.py           # Application entry point
├── requirements.txt  # Python dependencies
└── run_ats.bat      # Windows launcher script
```

## 🎮 Cara Penggunaan

### Menjalankan Aplikasi

**Windows:**
```bash
# Menggunakan batch file
run_ats.bat

# Atau langsung dengan Python
python main.py
```

**Linux/Mac:**
```bash
python main.py
```

### Menggunakan Interface

1. **Pencarian Dasar**
   - Masukkan kata kunci di field pencarian
   - Pilih algoritma (KMP/Boyer-Moore)
   - Klik "Search" untuk mencari

2. **Fuzzy Search**
   - Aktifkan "Enable Fuzzy Search"
   - Atur threshold similarity (0.0 - 1.0)
   - Lakukan pencarian seperti biasa

3. **Filter dan Sorting**
   - Gunakan dropdown untuk filter berdasarkan role
   - Atur jumlah hasil maksimum
   - Hasil otomatis diurutkan berdasarkan relevansi

4. **Analisis Performa**
   - Lihat waktu eksekusi di panel hasil
   - Bandingkan performa antar algoritma
   - Export hasil untuk analisis lebih lanjut

## 🧪 Testing

Jalankan test suite:
```bash
python -m pytest tests/
```

Test algoritma specific:
```bash
python tests/test_algorithms.py
```

## ⚙️ Konfigurasi

Edit file `config.py` untuk menyesuaikan:

```python
# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'ats_db'
}

# Application settings
APP_CONFIG = {
    'similarity_threshold': 0.7,
    'max_results': 50,
    'supported_formats': ['.pdf']
}
```

## 📊 Algoritma yang Diimplementasikan

### 1. Knuth-Morris-Pratt (KMP)
- **Kompleksitas**: O(n + m)
- **Kegunaan**: Pencarian exact match yang efisien
- **Kelebihan**: Tidak ada backtracking

### 2. Boyer-Moore
- **Kompleksitas**: O(n/m) best case, O(nm) worst case
- **Kegunaan**: Pencarian pattern yang efektif untuk teks panjang
- **Kelebihan**: Skip karakterter yang tidak cocok

### 3. Levenshtein Distance
- **Kompleksitas**: O(nm)
- **Kegunaan**: Fuzzy matching dengan toleransi error
- **Kelebihan**: Dapat menangani typo dan variasi kata

## 🔧 Troubleshooting

### Masalah Database
```bash
# Test koneksi database
python -c "from database.database import DatabaseConnection; db = DatabaseConnection(); print('✅ OK' if db.connect() else '❌ Failed')"
```

### Masalah Dependencies
```bash
# Reinstall semua dependencies
pip install -r requirements.txt --force-reinstall
```

### Masalah PDF Reading
- Pastikan PyMuPDF terinstall dengan benar
- Check permission file PDF
- Pastikan PDF tidak corrupt atau terenkripsi

## 👥 Tim Pengembang

- **Irgiansyah** - Lead Developer
- **[Nama Anggota 2]** - Algorithm Specialist  
- **[Nama Anggota 3]** - Database Designer

## 📝 Lisensi

Project ini dikembangkan untuk keperluan akademik Tugas Besar 3.

## 🚀 Future Enhancements

- [ ] Support format CV selain PDF (DOC, DOCX)
- [ ] Machine Learning untuk ranking yang lebih cerdas
- [ ] Web-based interface
- [ ] REST API endpoint
- [ ] Advanced analytics dan reporting
- [ ] Multi-language support

---

**⭐ Jika project ini bermanfaat, jangan lupa berikan star!**
