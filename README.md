<div align="center">

# 📈 59 Inflasi — Aplikasi Prediksi Inflasi Bulanan (Streamlit)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/GUI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/DL-TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Repo Size](https://img.shields.io/github/repo-size/useripx/59-Inflasi?style=for-the-badge&color=blue)
![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Selesai-brightgreen?style=for-the-badge)
![Semester](https://img.shields.io/badge/Semester-1-blueviolet?style=for-the-badge)

**Aplikasi web cerdas berbasis Machine Learning dan Deep Learning untuk memprediksi tingkat inflasi bulanan di Indonesia menggunakan NLP (TF-IDF) dan algoritma Regresi (Random Forest, XGBoost, LSTM, dll).**

*Dibuat oleh Yogi Ario Pratama — NPM: 2313020004 — Proyek Semester 1*

---

</div>

## 📖 Deskripsi

**Proyek 59 (Inflasi)** adalah aplikasi *web-based* yang dikembangkan menggunakan **Streamlit**. Aplikasi ini memungkinkan pengguna untuk memprediksi tingkat inflasi bulanan di masa depan dengan memasukkan parameter Bulan, Tahun, serta deskripsi teks "Penyebab Utama" (seperti "Kenaikan harga BBM"). Data teks ini kemudian diekstrak konteksnya menggunakan metode *Natural Language Processing* (NLP) yaitu `TfidfVectorizer`.

Model telah dilatih menggunakan data historis (`asset/Data Inflasi.xlsx`). Antarmuka aplikasi dibuat dengan desain *Glassmorphism* modern dengan palet warna gradien gelap dan aksen neon (*teal*).

## ✨ Fitur

- **Modern Premium UI** — Tampilan antarmuka menggunakan CSS khusus bergaya *Glassmorphism* untuk memberikan estetika yang memukau.
- **Natural Language Processing (NLP)** — Fitur ekstraksi teks otomatis dari input teks pengguna.
- **7 Algoritma AI (Machine Learning & Deep Learning)**:
  - Random Forest Regressor
  - XGBoost Regressor
  - Support Vector Regression (SVR)
  - Linear Regression
  - Prophet (oleh Meta)
  - SARIMA
  - LSTM (Long Short-Term Memory Neural Network)
- **Trainable Models** — Menyediakan skrip `train_models.py` untuk melatih dan mengekspor ulang model `.pkl` jika Anda memiliki dataset inflasi terbaru.

## 📁 Struktur Proyek

- `app.py`: Skrip utama yang menjalankan *web server* antarmuka Streamlit.
- `train_models.py`: Skrip *backend* untuk melatih dataset ke dalam 7 algoritma model ML/DL.
- `Prediksi_Inflasi.ipynb`: *Jupyter Notebook* untuk eksperimen dan Analisis Data Eksploratif (EDA).
- `models.pkl`: File terkompresi yang memuat objek model dan *TF-IDF Vectorizer* yang sudah dilatih (di-*train*).
- `asset/Data Inflasi.xlsx`: Dataset historis sumber inflasi.

## 🚀 Cara Menjalankan

### Prasyarat

- **Python 3.9+** terinstal.
- Disarankan menggunakan virtual environment (`venv`).
- Instal dependensi yang diperlukan:
  ```bash
  pip install -r requirements.txt
  ```

### Eksekusi

Untuk menjalankan aplikasi web:
```bash
streamlit run app.py
```
*(Aplikasi akan otomatis terbuka pada browser default Anda di `http://localhost:8501`)*

Jika ingin melatih ulang (re-train) model (memperbarui `models.pkl`):
```bash
python train_models.py
```

## 🛠️ Teknologi

| Komponen | Detail |
|----------|--------|
| Bahasa | Python 3.9+ |
| Framework UI | `streamlit` |
| Library Data | `pandas`, `numpy` |
| Machine Learning | `scikit-learn`, `xgboost`, `statsmodels`, `prophet` |
| Deep Learning | `tensorflow` (Keras LSTM) |
| Model Export | `pickle` |

---

## 👤 Author & Kontak

**Yogi Ario Pratama**

Jika Anda memiliki pertanyaan seputar kode ini atau ingin berdiskusi, silakan hubungi saya melalui WhatsApp:
📱 **[Chat via WhatsApp (wa.me/6281358113087)](https://wa.me/6281358113087)**

---

### 💖 Donasi

Dukungan Anda sangat berarti agar saya dapat terus semangat belajar dan mengembangkan proyek-proyek open-source lainnya. Jika berkenan memberikan donasi/apresiasi, Anda dapat menyalurkannya melalui:

💳 **Bank Seabank**

- No Rekening: **901497113744**
- Atas Nama: **Yogi Ario Pratama**

---

<div align="center">

*Proyek Mata Kuliah — Semester 1 — Teknik Informatika UNP*

</div>
