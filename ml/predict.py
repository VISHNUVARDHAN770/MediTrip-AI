import pandas as pd
import joblib

saved_artifacts = joblib.load("ml/recommendation_model.pkl")
model = saved_artifacts["model"]
preprocessor = saved_artifacts["preprocessor"]

def get_recommendations(user_city, user_symptom, max_user_budget):
    df = pd.read_csv("ml/dataset/hospital_data.csv")
    
    # 1. Filter by City, Symptom, and Budget Constraint
    filtered = df[
        (df["city"] == user_city) & 
        (df["symptom"].str.contains(user_symptom, case=False, na=False)) &
        (df["total_estimated_cost"] <= max_user_budget)
    ].copy()
    
    if filtered.empty:
        print(f"\n⚠️ No hospitals found in {user_city} for '{user_symptom}' within budget ₹{max_user_budget}")
        return
    
    # 2. Extract features and predict match score
    features = filtered[["city", "specialization", "consultation_fee", "estimated_meds_cost", "total_estimated_cost", "wait_time_mins", "hospital_rating", "doctor_exp_years", "distance_km", "insurance_accepted"]]
    processed_features = preprocessor.transform(features)
    filtered["predicted_match_score"] = model.predict(processed_features)
    
    # 3. Sort by highest match score
    ranked = filtered.sort_values(by="predicted_match_score", ascending=False)
    
    # Display Output
    sample = ranked.iloc[0]
    print("\n" + "="*65)
    print(f"🔍 PREDICTED DIAGNOSIS: {sample['predicted_disease']}")
    print(f"🩺 RECOMMENDED SPECIALTY: {sample['specialization']}")
    print(f"💰 BUDGET LIMIT: ₹{max_user_budget}")
    print("="*65)
    
    print("\n🏥 RANKED HOSPITAL RECOMMENDATIONS:")
    for idx, row in ranked.head(5).iterrows():
        print(f"\n🔹 {row['hospital_id']} | Match Score: {row['predicted_match_score']:.1f}%")
        print(f"   • Doctor Fee: ₹{row['consultation_fee']} | Estimated Meds: ₹{row['estimated_meds_cost']}")
        print(f"   • Approx Total Cost: ₹{row['total_estimated_cost']} | Rating: {row['hospital_rating']}⭐ | Distance: {row['distance_km']} km")

if __name__ == "__main__":
    # Test scenario: User in Vijayawada with Chest Pain and max budget ₹1,500
    get_recommendations(
        user_city="Vijayawada", 
        user_symptom="Chest Pain", 
        max_user_budget=1500
    )