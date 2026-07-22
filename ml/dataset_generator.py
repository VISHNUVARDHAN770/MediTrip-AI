import pandas as pd
import numpy as np
import os

os.makedirs("ml/dataset", exist_ok=True)
np.random.seed(42)

num_samples = 1200

cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Vijayawada", "Kadapa"]

# Mapping symptoms -> disease category -> recommended specialty
symptom_mapping = [
    {"symptom": "Chest Pain, Shortness of Breath", "disease": "Angina / Coronary Issue", "specialization": "Cardiology"},
    {"symptom": "Joint Pain, Swelling", "disease": "Arthritis / Fracture", "specialization": "Orthopedics"},
    {"symptom": "Severe Headache, Dizziness", "disease": "Migraine / Neurological Concern", "specialization": "Neurology"},
    {"symptom": "Unexplained Weight Loss, Fatigue", "disease": "Oncology Evaluation", "specialization": "Oncology"},
    {"symptom": "Stomach Pain, Acid Reflux", "disease": "Gastritis / Ulcer", "specialization": "Gastroenterology"}
]

languages = [
    "English, Hindi", 
    "English, Telugu", 
    "English, Tamil", 
    "English, Kannada", 
    "English, Hindi, Telugu"
]

data = []

for i in range(1, num_samples + 1):
    mapping = np.random.choice(symptom_mapping)
    city = np.random.choice(cities)
    
    # Cost Breakdown
    doc_fee = np.random.choice([200, 250, 300, 500, 800, 1000])
    estimated_meds_cost = np.random.randint(300, 3500)
    total_estimated_cost = doc_fee + estimated_meds_cost
    
    data.append({
        "hospital_id": f"HOSP_{i:04d}",
        "city": city,
        "symptom": mapping["symptom"],
        "predicted_disease": mapping["disease"],
        "specialization": mapping["specialization"],
        "consultation_fee": doc_fee,
        "estimated_meds_cost": estimated_meds_cost,
        "total_estimated_cost": total_estimated_cost,
        "wait_time_mins": np.random.randint(15, 90),
        "hospital_rating": np.round(np.random.uniform(3.5, 5.0), 1),
        "doctor_exp_years": np.random.randint(3, 30),
        "languages": np.random.choice(languages),
        "distance_km": np.round(np.random.uniform(0.5, 25.0), 1),
        "insurance_accepted": np.random.choice([1, 0], p=[0.8, 0.2]),
        "match_score": np.random.randint(60, 100)
    })

df = pd.DataFrame(data)
df.to_csv("ml/dataset/hospital_data.csv", index=False)
print("✅ Generated updated hospital_data.csv with symptom mapping and cost breakdowns!")