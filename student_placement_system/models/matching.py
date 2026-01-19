
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def calculate_utility(student, school, max_dist=50):
    """
    Calculates a utility score for a student-school pair.
    """
    # 1. Eligibility (Hard Constraint)
    if student['score'] < school['min_entry_score']:
        return -1 # Ineligible

    # 2. Preference Score (High weight)
    pref_score = 0
    if school['school_id'] == student['choice_1']:
        pref_score = 1.0
    elif school['school_id'] == student['choice_2']:
        pref_score = 0.7
    elif school['school_id'] == student['choice_3']:
        pref_score = 0.4

    # 3. Proximity Score
    dist = haversine(student['longitude'], student['latitude'], 
                     school['longitude'], school['latitude'])
    prox_score = max(0, 1 - (dist / max_dist)) # Normalized 0-1 within max_dist

    # 4. Equity/Fit Bonus
    equity_bonus = 0
    if student['disability'] == 1 and school['resources_score'] > 7:
        equity_bonus += 0.3
    if student['socioeconomic_status'] < 4 and school['school_type'] in ['National', 'Extra-County']:
        equity_bonus += 0.2

    # Total Utility
    # Weights: Pref=0.5, Prox=0.3, Equity=0.2
    total_score = (0.5 * pref_score) + (0.3 * prox_score) + (0.2 * equity_bonus)
    
    return total_score

def run_matching(students_df, schools_df):
    """
    Runs the matching algorithm.
    Returns updated students_df with 'assigned_school' and 'match_score'.
    """
    students_df = students_df.copy()
    schools_df = schools_df.copy()
    
    # Track capacity
    school_capacities = schools_df.set_index('school_id')['capacity'].to_dict()
    school_assignments = {sid: 0 for sid in school_capacities}
    
    # Store assignments
    assignments = {} # student_id -> school_id
    assignment_scores = {} # student_id -> score
    
    # We will compute utilities only for relevant schools to save time if needed,
    # but for 5000x50, we can do batch or just iterate "smartly".
    # Strategy: For each student, checking ALL schools is O(N*M). 5000*50 = 250k ops. Fast in Python.
    
    print("Calculating utilities...")
    potential_matches = []
    
    # Optimization: Vectorize or simple loop? Simple loop is readable for prototype.
    # Convert dataframes to dicts for speed
    students_list = students_df.to_dict('records')
    schools_list = schools_df.to_dict('records')
    
    for s in students_list:
        for sch in schools_list:
            u = calculate_utility(s, sch)
            if u >= 0:
                potential_matches.append({
                    'student_id': s['student_id'],
                    'school_id': sch['school_id'],
                    'utility': u
                })
    
    # Sort matches by utility descending (Global Optimization Strategy - Greedy)
    print("Sorting matches...")
    potential_matches.sort(key=lambda x: x['utility'], reverse=True)
    
    print("Assigning students...")
    assigned_student_ids = set()
    
    for match in potential_matches:
        sid = match['student_id']
        shid = match['school_id']
        
        if sid in assigned_student_ids:
            continue
            
        if school_assignments[shid] < school_capacities[shid]:
            assignments[sid] = shid
            assignment_scores[sid] = match['utility']
            school_assignments[shid] += 1
            assigned_student_ids.add(sid)
    
    # Handle unassigned students (Assign to nearest with space)
    unassigned = [s for s in students_list if s['student_id'] not in assigned_student_ids]
    print(f"Unassigned after primary pass: {len(unassigned)}")
    
    for s in unassigned:
        sid = s['student_id']
        # Find nearest school with space
        nearest = None
        min_dist = float('inf')
        
        for sch in schools_list:
            shid = sch['school_id']
            if school_assignments[shid] < school_capacities[shid]:
                 dist = haversine(s['longitude'], s['latitude'], sch['longitude'], sch['latitude'])
                 if dist < min_dist:
                     min_dist = dist
                     nearest = shid
        
        if nearest:
            assignments[sid] = nearest
            assignment_scores[sid] = 0.0 # Forced assignment
            school_assignments[nearest] += 1
            assigned_student_ids.add(sid)
    
    students_df['assigned_school'] = students_df['student_id'].map(assignments)
    students_df['match_score'] = students_df['student_id'].map(assignment_scores)
    
    return students_df
