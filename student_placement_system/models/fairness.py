
import pandas as pd
import numpy as np

def calculate_bias_metrics(students_df, schools_df):
    """
    Calculates fairness metrics for the placement.
    """
    # Merge school info to check quality of assignment
    merged = students_df.merge(schools_df, left_on='assigned_school', right_on='school_id', how='left')
    
    # Metric 1: Placement Rate by Gender (if we had unassigned, but we force assign)
    # Metric 2: "High Quality" School Assignment Rate by Group
    # Define "High Quality" as National or Extra-County
    
    merged['is_high_quality'] = merged['school_type'].isin(['National', 'Extra-County'])
    
    metrics = {}
    
    # Gender Fairness
    gender_group = merged.groupby('gender')['is_high_quality'].mean()
    metrics['gender_parity_ratio'] = gender_group['Female'] / gender_group['Male'] if 'Male' in gender_group and gender_group['Male'] > 0 else 0
    
    # Socioeconomic Fairness
    # Low SES (1-4) vs High SES (7-10)
    low_ses = merged[merged['socioeconomic_status'] <= 4]['is_high_quality'].mean()
    high_ses = merged[merged['socioeconomic_status'] >= 7]['is_high_quality'].mean()
    metrics['ses_disparity'] = low_ses / high_ses if high_ses > 0 else 0
    
    # Regional Fairness (Simplified: distance to school)
    avg_dist = merged.apply(lambda row: ((row['latitude_x'] - row['latitude_y'])**2 + (row['longitude_x'] - row['longitude_y'])**2)**0.5, axis=1).mean()
    metrics['avg_displacement'] = avg_dist # In degrees approx
    
    return metrics, merged
