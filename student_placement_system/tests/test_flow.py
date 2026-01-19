
import sys
import os
import pandas as pd

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.processing import load_data
from models.matching import run_matching
from models.prediction import predict_enrollment
from models.fairness import calculate_bias_metrics

def test_system():
    print("Testing Data Loading...")
    students, schools = load_data(regenerate=True)
    assert not students.empty
    assert not schools.empty
    print(f"Loaded {len(students)} students and {len(schools)} schools.")
    
    print("Testing Matching Engine...")
    placed_df = run_matching(students, schools)
    assert 'assigned_school' in placed_df.columns
    assert placed_df['assigned_school'].notna().all() # We forced assignment
    print("Matching completed successfully.")
    
    print("Testing Fairness Metrics...")
    metrics, _ = calculate_bias_metrics(placed_df, schools)
    print("Metrics:", metrics)
    assert 'gender_parity_ratio' in metrics
    
    print("Testing Prediction...")
    preds = predict_enrollment()
    assert not preds.empty
    print("Prediction run successfully.")
    
    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    test_system()
