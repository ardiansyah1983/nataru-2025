# 📡 Dashboard QoS Telekomunikasi - Version 5.0

## ✨ NEW: Auto-Read dari Folder 'data'

Dashboard sekarang **otomatis membaca file** dari folder `data` tanpa perlu upload manual!

---

## 🚀 Quick Start

### 1. Setup Folder

```bash
# Buat folder 'data' di direktori yang sama dengan qos_dashboard.py
mkdir data

# Copy file Excel atau CSV Anda ke folder data
# Windows:
copy "Data_QOS_Posko_Nataru_2025.xlsx" data\

# Linux/Mac:
cp Data_QOS_Posko_Nataru_2025.xlsx data/
```

### 2. Install Dependencies

```bash
pip install streamlit pandas plotly openpyxl xlrd numpy
```

### 3. Jalankan Dashboard

```bash
streamlit run qos_dashboard.py
```

### 4. Pilih File

Dashboard akan otomatis scan folder `data` dan menampilkan semua file yang tersedia!

---

## 📁 Struktur Folder

```
project/
├── qos_dashboard.py          # Dashboard utama
├── requirements.txt           # Dependencies
├── README.md                  # Dokumentasi ini
└── data/                      # Folder untuk file data
    ├── Data_QOS_2025.xlsx     # File 1
    ├── Data_QOS_2024.xlsx     # File 2
    └── Data_Export.csv        # File 3
```

---

## ✨ Fitur Baru V5.0

### 🔍 Auto-Scan Folder
- ✅ Otomatis scan folder `data`
- ✅ Deteksi file .xlsx, .xls, .csv
- ✅ Urutkan berdasarkan waktu modifikasi (terbaru di atas)
- ✅ Tampilkan info file (nama, ukuran, tanggal)

### 📂 Dual Source Mode
Dashboard mendukung 2 cara load data:

**Option 1: Dari Folder 'data' (Recommended)**
- Letakkan file di folder `data`
- Pilih dari dropdown
- Otomatis load

**Option 2: Upload Manual**
- Klik "Upload Manual"
- Browse file dari komputer
- Upload dan load

### 📊 File Info Display
```
📄 File Info:
📝 Nama: Data_QOS_Posko_Nataru_2025.xlsx
📊 Ukuran: 1.23 MB
🕐 Modified: 2025-01-04 10:30:15
```

---

## 🎯 Cara Menggunakan

### Scenario 1: Analisis Single File

```bash
# 1. Copy file ke folder data
cp my_qos_data.xlsx data/

# 2. Run dashboard
streamlit run qos_dashboard.py

# 3. Dashboard otomatis detect file
# 4. Pilih file dari dropdown
# 5. Data otomatis loaded!
```

### Scenario 2: Bandingkan Multiple Files

```bash
# 1. Copy beberapa file
cp data_januari.xlsx data/
cp data_februari.xlsx data/
cp data_maret.xlsx data/

# 2. Run dashboard
streamlit run qos_dashboard.py

# 3. Pilih file dari dropdown
# 4. Ganti file dengan dropdown untuk compare
```

### Scenario 3: Upload File Baru

```bash
# 1. Run dashboard
streamlit run qos_dashboard.py

# 2. Pilih "Upload Manual" di sidebar
# 3. Browse & upload file
# 4. Analisis file yang baru diupload
```

---

## 📊 Format File yang Didukung

### Excel (.xlsx, .xls)
```
✅ Format modern (.xlsx)
✅ Format legacy (.xls)
✅ Auto-detect sheet 'Compile_Summary'
✅ Fallback ke sheet pertama jika tidak ada
```

### CSV (.csv)
```
✅ Comma-separated values
✅ UTF-8 encoding
✅ Headers required
```

### Required Columns
```
✓ Operator
✓ Kabupaten / Kota
✓ Lokasi Pengukuran
```

---

## 💡 Tips & Best Practices

### Naming Convention
```
✅ GOOD:
  - Data_QOS_2025_Januari.xlsx
  - QOS_Nataru_2025.xlsx
  - Measurement_Results.csv

❌ AVOID:
  - data.xlsx (terlalu generic)
  - file1.csv (tidak deskriptif)
  - qos 2025.xlsx (spasi di nama file)
```

### File Organization
```
data/
├── 2025/
│   ├── January_QOS.xlsx
│   ├── February_QOS.xlsx
│   └── March_QOS.xlsx
└── 2024/
    └── Annual_QOS.xlsx

# Gunakan subfolder untuk organisasi yang lebih baik
```

### Performance
```
✅ File size < 10 MB: Optimal
⚠️ File size 10-50 MB: Masih OK
❌ File size > 50 MB: Might be slow

Tip: Filter data di Excel sebelum save ke folder 'data'
```

---

## 🔧 Troubleshooting

### Problem: "Tidak ada file di folder 'data'"

**Solution:**
```bash
# Check apakah folder ada
ls data/

# Jika tidak ada, buat folder
mkdir data

# Copy file
cp your_file.xlsx data/

# Refresh browser
```

### Problem: "File tidak muncul di dropdown"

**Solution:**
```bash
# Check ekstensi file
ls -la data/

# Harus .xlsx, .xls, atau .csv
# Rename jika perlu:
mv data/file.XLSX data/file.xlsx

# Refresh dashboard
```

### Problem: "Error loading data"

**Solution:**
1. Check format file (harus valid Excel/CSV)
2. Pastikan ada sheet 'Compile_Summary' (untuk Excel)
3. Pastikan kolom required ada
4. Coba upload manual untuk debug

---

## 📈 Workflow Recommended

### Daily Analysis
```
1. Export data QoS ke Excel
2. Copy ke folder data/
3. Run dashboard
4. Select file dari dropdown
5. Analyze → Export charts
6. Repeat untuk hari berikutnya
```

### Weekly Report
```
1. Collect semua file mingguan di data/
2. Run dashboard
3. Loop through files via dropdown
4. Compare metrics week-over-week
5. Generate conclusions
6. Create report
```

### Monthly Comparison
```
1. Archive old files ke subfolder
2. Keep current month in data/
3. Use dropdown untuk compare
4. Identify trends
5. Make recommendations
```

---

## 🎨 Fitur Dashboard

### 7 Tab Lengkap
| Tab | Fitur |
|-----|-------|
| 📊 Overview | Distribusi, top lokasi, summary |
| 📡 Signal | RSRP, RSRQ, SINR (4G & 2G) |
| 🚀 Speed | DL/UL speed, Browsing |
| 📹 YouTube | SR, TTFP, Latency |
| 🔄 4G vs 2G | Technology comparison |
| 📍 Lokasi | Detail per lokasi dengan radar chart |
| 📋 Kesimpulan | Auto-generated insights |

### Filter Interaktif
- ✅ Kabupaten/Kota
- ✅ Lokasi Pengukuran
- ✅ Operator (Indosat, Telkomsel, XL)

### Operator Colors
- 🟡 Indosat → Yellow
- 🔴 Telkomsel → Red
- 🔵 XL → Blue

---

## 🆕 What's New in V5.0?

### Before (V4.0)
```
❌ Manual upload setiap kali
❌ Tidak bisa switch file
❌ Harus re-upload untuk compare
```

### After (V5.0)
```
✅ Auto-scan folder 'data'
✅ Dropdown selection
✅ Easy file switching
✅ File info display
✅ Dual source mode
```

---

## 📦 Files Included

| File | Size | Description |
|------|------|-------------|
| `qos_dashboard.py` | 52KB | Main dashboard (V5.0) |
| `requirements.txt` | 89B | Dependencies |
| `README.md` | This | Documentation |
| `SETUP_GUIDE.md` | - | Detailed setup guide |

---

## 🎯 Version History

| Version | Feature | Status |
|---------|---------|--------|
| v1.0 | Initial | ❌ Had errors |
| v2.0 | Partial fix | ❌ Still errors |
| v3.0 | Better | ❌ Not perfect |
| v4.0 | Redesigned | ✅ Working |
| **v5.0** | **Auto-read folder** | ✅ **BEST!** |

---

## ✅ Production Ready!

Dashboard V5.0 adalah versi terbaik dengan:
- ✅ Zero errors
- ✅ Auto-read dari folder
- ✅ Dual source mode
- ✅ Complete features
- ✅ Professional quality

---

## 🚀 Get Started Now!

```bash
# 1. Setup
mkdir data
cp your_data.xlsx data/

# 2. Install
pip install -r requirements.txt

# 3. Run
streamlit run qos_dashboard.py

# 4. Enjoy! 🎉
```

---

**Version**: 5.0 Final  
**Status**: ✅ Production Ready  
**Quality**: ⭐⭐⭐⭐⭐  

**Happy Analyzing! 📡📊🚀**