# Fashion-Lens-Upload-Get-Recommendations

Aplikasi fashion recommendation yang menggunakan **image feature extraction** dengan ResNet50. Upload gambar pakaian Anda dan dapatkan rekomendasi pakaian serupa dari database.

## 🎯 Fitur

- **Upload Gambar**: Upload gambar pakaian melalui interface Streamlit yang user-friendly
- **Feature Extraction**: Menggunakan ResNet50 pre-trained untuk ekstraksi fitur gambar
- **Recommendation Engine**: K-Means clustering untuk menemukan pakaian yang paling mirip
- **Analisis Warna**: Deteksi warna dominan dari gambar yang diupload
- **API Backend**: Flask REST API untuk processing gambar
- **Frontend**: Streamlit untuk interface yang interaktif

---

## 📋 Prerequisites

Pastikan sudah install:
- **Python 3.8+**
- **pip** atau **conda** package manager
- **Git**

---

## 🚀 Cara Setup & Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/RafaXzaviero/Fashion-Lens-Upload-Get-Recommendations.git
cd Fashion-Lens-Upload-Get-Recommendations
```

### 2. Buat Virtual Environment

**Untuk macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Untuk Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

Upgrade pip terlebih dahulu:
```bash
pip install --upgrade pip
```

Install semua dependencies:
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install flask pandas pillow numpy scikit-learn torch torchvision streamlit requests
```

### 4. Persiapan Data

Pastikan file-file ini sudah ada di folder root:
- `shirts_only.csv` - Dataset pakaian
- `images.csv` - Mapping gambar ke product ID
- `shirt_features.pkl` - Pre-extracted features (optional)

### 5. Menjalankan Aplikasi

Aplikasi ini memiliki 2 komponen yang harus berjalan bersamaan:

#### A. Jalankan Flask Backend (di terminal 1)
```bash
python app.py
```

Output yang diharapkan:
```
* Running on http://127.0.0.1:5001
```

#### B. Jalankan Streamlit Frontend (di terminal 2)
```bash
streamlit run streamlit_app.py
```

Output yang diharapkan:
```
Local URL: http://localhost:8501
Network URL: http://xxx.xxx.xxx.xxx:8501
```

---

## 📖 Cara Menggunakan

1. **Buka Streamlit App** di browser: `http://localhost:8501`

2. **Upload Gambar**:
   - Klik tombol "Pilih gambar pakaian"
   - Pilih file gambar (format: JPG, PNG, JPEG)
   - Ukuran file maksimal 200MB

3. **Dapatkan Rekomendasi**:
   - Aplikasi akan menganalisis gaya pakaian
   - Menampilkan rekomendasi pakaian serupa dari database
   - Lihat detail dan fitur yang sesuai

4. **Ubah API URL** (jika diperlukan):
   - Di sidebar kiri, masukkan Flask API URL
   - Default: `http://127.0.0.1:5001/upload_image`

---

## 🛠️ Troubleshooting

### Error: "Connection refused" / API tidak terhubung
**Solusi:**
- Pastikan Flask backend sudah berjalan (`python app.py`)
- Periksa port 5001 tidak ter-block
- Pastikan URL di Streamlit sidebar benar

### Error: "ModuleNotFoundError"
**Solusi:**
- Pastikan virtual environment sudah aktif
- Install ulang dependencies: `pip install -r requirements.txt`

### Gambar tidak diproses
**Solusi:**
- Pastikan format gambar: JPG, PNG, atau JPEG
- Cek ukuran file tidak terlalu besar
- Lihat console backend untuk error messages

---

## 📁 Project Structure

```
Fashion-Lens-Upload-Get-Recommendations/
├── app.py                    # Flask backend API
├── streamlit_app.py          # Streamlit frontend
├── shirts_only.csv           # Dataset pakaian
├── images.csv                # Image mapping
├── styles.csv                # Style classification
├── shirt_features.pkl        # Pre-extracted features
└── README.md                 # Dokumentasi ini
```

---

## 🔧 API Endpoints

### POST `/upload_image`
Upload gambar dan dapatkan rekomendasi.

**Request:**
```
- Method: POST
- Content-Type: multipart/form-data
- Body: image (file)
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": 123,
      "name": "Product Name",
      "similarity_score": 0.95,
      "color": "Blue",
      "image_url": "url_to_image"
    }
  ],
  "dominant_color": "Blue"
}
```

---

## 📊 Tech Stack

- **Backend**: Flask
- **Frontend**: Streamlit
- **ML/DL**: PyTorch, ResNet50, scikit-learn
- **Data Processing**: Pandas, NumPy, Pillow
- **Clustering**: K-Means

---

## ⚠️ Notes

- Model ResNet50 akan di-download otomatis pada first run
- Feature extraction menggunakan GPU jika tersedia, CPU jika tidak
- Rekomendasi berdasarkan visual similarity dan dominant color
- Untuk production, gunakan gunicorn untuk Flask daripada development server

---

## 👤 Author

**RafaXzaviero**

---

## 📝 License

MIT License - silahkan gunakan dan modifikasi sesuai kebutuhan
