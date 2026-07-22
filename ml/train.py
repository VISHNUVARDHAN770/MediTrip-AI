import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor

dataset_path = "ml/dataset/hospital_data.csv"
if not os.path.exists(dataset_path):
    raise FileNotFoundError("Run 'python ml/dataset_generator.py' first!")

df = pd.read_csv(dataset_path)

# Features including detailed costs
X = df[["city", "specialization", "consultation_fee", "estimated_meds_cost", "total_estimated_cost", "wait_time_mins", "hospital_rating", "doctor_exp_years", "distance_km", "insurance_accepted"]]
y = df["match_score"]

categorical_cols = ["city", "specialization"]
numerical_cols = ["consultation_fee", "estimated_meds_cost", "total_estimated_cost", "wait_time_mins", "hospital_rating", "doctor_exp_years", "distance_km", "insurance_accepted"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numerical_cols)
    ]
)

X_processed = preprocessor.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

print("⏳ Training XGBoost Model with Cost & Symptom Engine...")
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

model_path = "ml/recommendation_model.pkl"
joblib.dump({"model": model, "preprocessor": preprocessor}, model_path)
print(f"📦 Model saved successfully to {model_path}!")