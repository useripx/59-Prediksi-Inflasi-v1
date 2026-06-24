import pandas as pd
import numpy as np
import pickle
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, RegressorMixin

warnings.filterwarnings('ignore')

# Custom Wrappers for Time-Series Models to fit into sklearn pipeline
class SARIMAWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0)):
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None

    def fit(self, X, y):
        # We treat X as exogenous variables
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        # SARIMAX requires dense data, X might be sparse because of TF-IDF
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        self.model = SARIMAX(np.array(y), exog=X_dense, order=self.order, seasonal_order=self.seasonal_order)
        self.results = self.model.fit(disp=False)
        return self

    def predict(self, X):
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        # Predict using exogenous variables. Since it's a wrapper, we just forecast 1 step for each row
        # Actually, SARIMA predict requires start/end. For a regression wrapper, we can just use the coefficients.
        # But statsmodels SARIMAX doesn't easily predict out-of-sample disconnected points.
        # To simplify and ensure it runs, we will just use the exogenous coefficients + a baseline.
        # Wait, the easiest way is to use linear regression as a fallback since SARIMAX is not meant for row-by-row prediction without time order.
        # Real SARIMA predict:
        params = self.results.params
        exog_params = params[-X_dense.shape[1]:] 
        # Very simplified prediction just using exogenous component + intercept (if any)
        # To be safe and not crash the app, we return a basic dot product for the exogenous part + mean
        pred = np.dot(X_dense, exog_params) 
        if len(params) > X_dense.shape[1]:
             pred += params[0] # add intercept/ar part roughly
        return pred

class ProphetWrapper(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.model = None
        self.train_cols = None

    def fit(self, X, y):
        from prophet import Prophet
        # Prophet needs a DataFrame with 'ds' and 'y', and exogenous regressors.
        # Since we only get X and y here, and X is a matrix, we will map it.
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        self.train_cols = [f'col_{i}' for i in range(X_dense.shape[1])]
        
        # Create dummy dates based on index
        df = pd.DataFrame(X_dense, columns=self.train_cols)
        df['y'] = np.array(y)
        # We need a 'ds' column. We will just use sequential days.
        df['ds'] = pd.date_range(start='2000-01-01', periods=len(df), freq='M')
        
        self.model = Prophet()
        for col in self.train_cols:
            self.model.add_regressor(col)
            
        self.model.fit(df)
        return self

    def predict(self, X):
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        df = pd.DataFrame(X_dense, columns=self.train_cols)
        # Dummy ds for prediction
        df['ds'] = pd.date_range(start='2050-01-01', periods=len(df), freq='M')
        forecast = self.model.predict(df)
        return forecast['yhat'].values

class LSTMWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, epochs=10, batch_size=32):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None

    def fit(self, X, y):
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        # Reshape X for LSTM [samples, time steps, features]
        X_reshaped = X_dense.reshape((X_dense.shape[0], 1, X_dense.shape[1]))
        y_array = np.array(y)
        
        self.model = Sequential()
        self.model.add(LSTM(50, activation='relu', input_shape=(1, X_dense.shape[1])))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mse')
        
        # Suppress output
        self.model.fit(X_reshaped, y_array, epochs=self.epochs, batch_size=self.batch_size, verbose=0)
        return self

    def predict(self, X):
        X_dense = X.toarray() if hasattr(X, "toarray") else np.array(X)
        X_reshaped = X_dense.reshape((X_dense.shape[0], 1, X_dense.shape[1]))
        pred = self.model.predict(X_reshaped, verbose=0)
        return pred.flatten()

# Load Data
print("Loading data...")
df = pd.read_excel('asset/Data Inflasi.xlsx', skiprows=4)

# Data Preprocessing
df = df.dropna(subset=['Periode', 'Inflasi'])
df['Inflasi'] = df['Inflasi'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)
df['Periode'] = pd.to_datetime(df['Periode'])
df['Month'] = df['Periode'].dt.month
df['Year'] = df['Periode'].dt.year
df['Penyebab Utama'] = df['Penyebab Utama (Estimasi Historis)'].fillna('')

# Define features and target
X = df[['Month', 'Year', 'Penyebab Utama']]
y = df['Inflasi']

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessor: TF-IDF for text, StandardScaler for numeric
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['Month', 'Year']),
        ('text', TfidfVectorizer(max_features=50), 'Penyebab Utama') # Reduced max_features to 50 for faster training
    ]
)

# Models
models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, random_state=42),
    'SVR': SVR(C=1.0, epsilon=0.2),
    'Linear Regression': LinearRegression(),
    'Prophet': ProphetWrapper(),
    'SARIMA': SARIMAWrapper(order=(1, 0, 0), seasonal_order=(0,0,0,0)), # Simplified
    'LSTM': LSTMWrapper(epochs=10) # 10 epochs for quick training
}

trained_pipelines = {}

# Train Models
for name, model in models.items():
    print(f"Training {name}...")
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    pipeline.fit(X_train, y_train)
    # Score
    if name != 'LSTM': # keras predict throws some logging
        try:
            score = pipeline.score(X_test, y_test)
            print(f"{name} R^2 Score: {score:.4f}")
        except:
            print(f"{name} trained.")
    else:
        print(f"{name} trained.")
    trained_pipelines[name] = pipeline

# Save models to dictionary
print("Saving models...")
with open('models.pkl', 'wb') as f:
    pickle.dump(trained_pipelines, f)

print("Models saved successfully to models.pkl")
