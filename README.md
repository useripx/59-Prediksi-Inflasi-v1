# 📈 Prediksi Inflasi Bulanan App

![Repo Size](https://img.shields.io/github/repo-size/useripx/Prediksi-Inflasi-v1.git?style=flat-square&color=blue)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat-square&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=flat-square&logo=TensorFlow&logoColor=white)

Aplikasi web cerdas berbasis Machine Learning dan Deep Learning untuk memprediksi tingkat inflasi bulanan di Indonesia. Pengguna dapat memilih Bulan, Tahun, dan memasukkan penyebab utama inflasi secara tekstual. Aplikasi ini secara otomatis mengekstrak fitur NLP menggunakan *TF-IDF* dan memberikan hasil prediksi dengan antarmuka yang sangat modern (*Glassmorphism*).

## ✨ Fitur Utama

- **Antarmuka Premium Modern**: Menggunakan desain *Glassmorphism* dan warna gradasi untuk memberikan tampilan masa kini yang jauh dari kesan generik aplikasi Streamlit standar.
- **7 Algoritma Machine Learning & Deep Learning**:
  - Random Forest Regressor
  - XGBoost Regressor
  - SVR (Support Vector Regression)
  - Linear Regression
  - Prophet (oleh Meta)
  - SARIMA
  - LSTM (Long Short-Term Memory)
- **Natural Language Processing (NLP)**: Fitur ekstraksi otomatis teks menggunakan `TfidfVectorizer` untuk mengambil konteks dari kolom "Penyebab Utama".
- **Eksperimen Terbuka**: Termasuk file Jupyter Notebook (`Prediksi_Inflasi.ipynb`) untuk melihat proses eksplorasi data (*EDA*) dan proses *training* model.

## 🚀 Cara Menjalankan Secara Lokal

1. **Clone repository ini** (setelah Anda mengunggahnya ke GitHub):
   ```bash
   git clone https://github.com/useripx/Prediksi-Inflasi-v1.git
   cd prediksi-inflasi-app
   ```

2. **Buat Virtual Environment (Opsional namun direkomendasikan)**:
   ```bash
   python -m venv env
   # Di Windows
   env\Scripts\activate
   # Di Mac/Linux
   source env/bin/activate
   ```

3. **Install *dependencies***:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi Streamlit**:
   ```bash
   streamlit run app.py
   ```

Aplikasi akan secara otomatis terbuka di peramban (browser) web Anda melalui `http://localhost:8501`.

## 🛠️ Modifikasi Model

Jika Anda memiliki data baru (versi *update* dari `Data Inflasi.xlsx`) dan ingin melatih ulang (re-train) model, Anda cukup menjalankan skrip:

```bash
python train_models.py
```

Skrip ini akan memperbarui file `models.pkl` dengan model terbaru yang sudah dilatih dengan data yang Anda sediakan.

## 📄 Struktur Direktori
- `app.py`: File utama menjalankan server web Streamlit.
- `train_models.py`: Skrip untuk melatih 7 jenis algoritma ML dan Deep Learning.
- `Prediksi_Inflasi.ipynb`: Jupyter notebook untuk eksplorasi dan percobaan dataset.
- `requirements.txt`: Daftar seluruh dependensi pustaka Python.
- `asset/Data Inflasi.xlsx`: Dataset historis yang digunakan.
- `models.pkl`: *File Pickle* yang menyimpan model terlatih dan TF-IDF Vectorizer.
