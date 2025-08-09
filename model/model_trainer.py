import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

# Generate synthetic time-series data
np.random.seed(42)
n_samples = 1000
X = np.random.randn(n_samples, 2)

# Introduce some anomalies
n_anomalies = 50
X[:n_anomalies] = 5 * np.random.randn(n_anomalies, 2)

df = pd.DataFrame(X, columns=['feature1', 'feature2'])

# Train the Isolation Forest model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df)

# Save the trained model
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/anomaly_model.joblib')
print("Model trained and saved to 'model/anomaly_model.joblib'")