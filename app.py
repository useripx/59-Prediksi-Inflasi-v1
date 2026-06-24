import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.base import BaseEstimator, RegressorMixin

# --- Class Wrappers (Harus ada agar pickle bisa load model) ---
class SARIMAWrapper(BaseEstimator, RegressorMixin):
    pass

class ProphetWrapper(BaseEstimator, RegressorMixin):
    pass

class LSTMWrapper(BaseEstimator, RegressorMixin):
    pass

# Karena kita butuh implementasi asli untuk predict, mari copy implementasinya
class SARIMAWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None

    def fit(self, X, y):
        pass # Not used in app.py
        
    def predict(self, X):
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        params = self.results.params
        exog_params = params[-X_dense.shape[1]:] 
        pred = np.dot(X_dense, exog_params) 
        if len(params) > X_dense.shape[1]:
             pred += params[0]
        return pred

class ProphetWrapper(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.model = None
        self.train_cols = None

    def fit(self, X, y):
        pass

    def predict(self, X):
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        df = pd.DataFrame(X_dense, columns=self.train_cols)
        df['ds'] = pd.date_range(start='2050-01-01', periods=len(df), freq='M')
        forecast = self.model.predict(df)
        return forecast['yhat'].values

class LSTMWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, epochs=10, batch_size=32):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None

    def fit(self, X, y):
        pass

    def predict(self, X):
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        X_reshaped = X_dense.reshape((X_dense.shape[0], 1, X_dense.shape[1]))
        pred = self.model.predict(X_reshaped, verbose=0)
        return pred.flatten()


# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Prediksi Inflasi Bulanan",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS untuk UI Modern (Glassmorphism & Clean) ---
st.markdown("""
    <style>
        /* Menggunakan font Poppins */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }

        /* Warna Latar Belakang & Teks Utama */
        .stApp {
            background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
            color: #ffffff;
        }

        /* Glassmorphism Container */
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 20px;
        }

        /* Header Title */
        .main-title {
            text-align: center;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 5px;
            font-size: 2.5rem;
        }
        .sub-title {
            text-align: center;
            font-weight: 300;
            color: #d1d1d1;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }

        /* Prediction Result Text */
        .result-text {
            text-align: center;
            font-size: 3rem;
            font-weight: 600;
            color: #00e5ff; /* Aksent Teal/Neon */
            text-shadow: 0px 0px 10px rgba(0, 229, 255, 0.6);
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- Judul Halaman ---
st.markdown('<h1 class="main-title">📈 Prediksi Inflasi Bulanan</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Pilih parameter di bawah ini untuk memprediksi tingkat inflasi dengan berbagai algoritma</p>', unsafe_allow_html=True)

# --- Load Models ---
@st.cache_resource
def load_models():
    try:
        import __main__
        # Patch __main__ to have the classes since pickle might look for them there
        setattr(__main__, "SARIMAWrapper", SARIMAWrapper)
        setattr(__main__, "ProphetWrapper", ProphetWrapper)
        setattr(__main__, "LSTMWrapper", LSTMWrapper)
        
        with open('models.pkl', 'rb') as f:
            models = pickle.load(f)
        return models
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None

models = load_models()

if models:
    # --- Input Section ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Pilihan Bulan
        month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                       "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        selected_month_name = st.selectbox("📅 Pilih Bulan", month_names)
        selected_month = month_names.index(selected_month_name) + 1
        
    with col2:
        # Pilihan Tahun
        years = list(range(2026, 2036))
        selected_year = st.selectbox("📆 Pilih Tahun", years)
        
    # Pilihan Algoritma
    algorithms = list(models.keys())
    selected_algorithm = st.selectbox("🧠 Pilih Algoritma Prediksi", algorithms)

    # Input Penyebab Utama
    penyebab_utama = st.text_area("📝 Penyebab Utama (Opsional)", 
                                  placeholder="Contoh: 'Kenaikan harga BBM' atau 'Peningkatan konsumsi jelang hari raya'")

    # Tombol Prediksi
    predict_button = st.button("🚀 Prediksi Inflasi", use_container_width=True)

    # --- Prediction Logic ---
    if predict_button:
        with st.spinner(f"Memproses prediksi dengan algoritma {selected_algorithm}..."):
            try:
                # Siapkan input data
                input_data = pd.DataFrame({
                    'Month': [selected_month],
                    'Year': [selected_year],
                    'Penyebab Utama': [penyebab_utama]
                })

                # Prediksi
                model_pipeline = models[selected_algorithm]
                prediction = model_pipeline.predict(input_data)[0]

                # Tampilkan Hasil
                st.markdown(f'''
                <div class="glass-card">
                    <h3 style="text-align: center; color: white;">Hasil Prediksi menggunakan <span style="color: #00e5ff;">{selected_algorithm}</span></h3>
                    <p class="result-text">{prediction:.2f}%</p>
                </div>
                ''', unsafe_allow_html=True)
                
                if prediction > 5.0:
                    st.warning("⚠️ Tingkat inflasi diprediksi cukup tinggi. Hal ini mungkin dipengaruhi oleh faktor musiman atau penyebab utama yang signifikan.")
                elif prediction < 1.5:
                    st.info("ℹ️ Tingkat inflasi diprediksi sangat rendah.")
                else:
                    st.success("✅ Tingkat inflasi diprediksi stabil.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")
else:
    st.warning("Model tidak ditemukan. Pastikan Anda telah men-train model.")
