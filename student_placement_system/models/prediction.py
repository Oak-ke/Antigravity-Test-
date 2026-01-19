
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_enrollment(years=5):
    """
    Simulates historical data and predicts future enrollment trends.
    """
    # Simulate last 10 years of data
    current_year = 2025
    years_hist = np.arange(current_year - 10, current_year).reshape(-1, 1)
    
    # Base trend: Growing population
    enrollment_hist = [500000 + (i * 20000) + np.random.randint(-5000, 5000) for i in range(10)]
    
    model = LinearRegression()
    model.fit(years_hist, enrollment_hist)
    
    future_years = np.arange(current_year, current_year + years).reshape(-1, 1)
    predictions = model.predict(future_years)
    
    return pd.DataFrame({
        'Year': future_years.flatten(),
        'Predicted_Enrollment': predictions.astype(int)
    })
