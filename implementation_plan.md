# Prediksi Inflasi Bulanan - Implementation Plan

Tujuan dari proyek ini adalah membangun aplikasi berbasis web modern menggunakan **Streamlit** dan membuat **Jupyter Notebook** (`.ipynb`) untuk memprediksi tingkat inflasi bulanan di Indonesia berdasarkan data historis yang diberikan (`Data Inflasi.xlsx`). 

Berdasarkan *feedback* pengguna, aplikasi ini akan memungkinkan pengguna untuk memilih **Bulan** dan **Tahun** melalui *dropdown*, memasukkan **Penyebab Utama** secara tekstual, dan memilih **Algoritma Prediksi** (Multi-Algoritma) dari *dropdown* untuk melihat perbandingan hasil prediksi.

## Rekomendasi Algoritma & Fitur

Karena sekarang kita juga menggunakan fitur teks (Penyebab Utama), pendekatannya murni berbasis **Regresi Machine Learning**, dengan ekstraksi fitur sebagai berikut:
1. **Bulan** (Numerik 1-12)
2. **Tahun** (Numerik)
3. **Penyebab Utama** (Diekstraksi menggunakan `TfidfVectorizer` untuk mengubah teks menjadi representasi numerik).

### Multi-Algoritma yang Akan Disediakan
Aplikasi akan melatih dan menyediakan beberapa pilihan algoritma di *dropdown* agar user bisa membandingkan:
1. **Random Forest Regressor**: Algoritma ansambel berbasis *decision tree* yang tangguh untuk data tabular dan kombinasi fitur teks.
2. **XGBoost Regressor**: Algoritma *boosting* yang seringkali memberikan akurasi tertinggi untuk masalah regresi.
3. **Support Vector Regression (SVR)**: Sangat baik untuk menangani data berdimensi tinggi (yang dihasilkan oleh fitur TF-IDF).
4. **Linear Regression**: Sebagai *baseline* sederhana untuk melihat apakah hubungan antar variabel bersifat linier.
5. **Prophet**: Algoritma deret waktu (time-series) tangguh buatan Meta.
6. **ARIMA / SARIMA**: Algoritma statistika klasik untuk deret waktu dengan pola musiman.
7. **LSTM (Long Short-Term Memory)**: Jaringan saraf tiruan (Deep Learning) yang optimal untuk memprediksi data sekuensial atau deret waktu.

## Desain UI / UX (Modern & Human-Made)

Agar tidak terlihat kaku atau generik seperti aplikasi Streamlit bawaan, kita akan mengimplementasikan:
- **Custom CSS Inject**: Mengubah font (menggunakan *Google Fonts* seperti Poppins), menghaluskan sudut kotak (border-radius), dan memberi efek transisi (hover effect).
- **Glassmorphism & Card Design**: Menggunakan kontainer layaknya "kartu" transparan dengan layout rapi. Input berada di sebelah kiri (atau form rapi di tengah), dan hasil prediksi berada di kartu *highlight* berukuran besar.
- **Palet Warna Premium**: Menggunakan palet *Dark Mode* elegan (seperti warna slate-gray gelap) dengan aksen *Neon/Teal* untuk metrik prediksi, atau mode bersih profesional.
- **Form Interaktif**: Penggunaan *dropdown* (`st.selectbox`) untuk Bulan, Tahun, dan Algoritma untuk mempercepat input pengguna. `st.text_area` untuk input "Penyebab Utama".

## Rencana Implementasi

Berikut adalah susunan file yang akan kita buat:

### 1. Eksplorasi & Pembuatan Model (`Prediksi_Inflasi.ipynb`)
- **[NEW]** `Prediksi_Inflasi.ipynb`: Notebook Jupyter yang memuat langkah-langkah:
  1. *Data Loading*: Membaca file `.xlsx`.
  2. *Data Preprocessing*: 
     - Menghapus tanda `%` dari kolom inflasi dan mengonversi menjadi numerik.
     - Mengekstrak `Bulan` dan `Tahun` dari kolom `Periode`.
  3. *Feature Engineering*: Membangun *pipeline* atau menggunakan `TfidfVectorizer` untuk teks "Penyebab Utama".
  4. *Model Training*: Melatih Random Forest, XGBoost, SVR, Linear Regression, Prophet, SARIMA, dan LSTM.
  5. *Model Export*: Menyimpan model-model tersebut ke format yang sesuai (`.pkl` atau `.h5` untuk LSTM).

### 2. Aplikasi Web Streamlit (`app.py`)
- **[NEW]** `app.py`: Skrip utama aplikasi Streamlit yang:
  - Memuat model-model dari file `.pkl`.
  - Menampilkan antarmuka UI dengan gaya *Glassmorphism/Modern*.
  - Menampilkan form *dropdown* (Bulan, Tahun, Algoritma) dan teks input (Penyebab Utama).
  - Melakukan pra-pemrosesan (TF-IDF) secara *real-time* dari teks input user.
  - Menampilkan prediksi angka inflasi.

### 3. Persiapan Deployment (GitHub & Streamlit Cloud)
- **[NEW]** `requirements.txt`: Mendaftar seluruh *library* yang diperlukan (`streamlit`, `pandas`, `scikit-learn`, `xgboost`, `openpyxl`, `prophet`, `statsmodels`, `tensorflow`).

## Verification Plan
1. Menjalankan `Prediksi_Inflasi.ipynb` secara utuh.
2. Memeriksa file `.pkl` berhasil dibuat.
3. Menjalankan `streamlit run app.py` dan mencoba seluruh form dengan kombinasi algoritma yang berbeda.
