
import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
np.random.seed(42)

def generate_schools(n_schools=50):
    """
    Generates a DataFrame of schools with location, capacity, and type.
    """
    schools = []
    types = ['National', 'Extra-County', 'County', 'Sub-County']
    
    # Simulate central location (e.g., Nairobi) to create some clusters
    center_lat, center_lon = -1.2921, 36.8219
    
    for i in range(n_schools):
        s_type = np.random.choice(types, p=[0.1, 0.2, 0.3, 0.4])
        
        # Capacity varies by type
        if s_type == 'National':
            capacity = random.randint(300, 600)
            min_score = 350
        elif s_type == 'Extra-County':
            capacity = random.randint(200, 400)
            min_score = 300
        else:
            capacity = random.randint(100, 300)
            min_score = 0

        # Location: disperse around center
        lat = center_lat + np.random.normal(0, 0.5) 
        lon = center_lon + np.random.normal(0, 0.5)

        schools.append({
            'school_id': f'S{i+1000}',
            'school_name': f"{fake.last_name()} {random.choice(['High', 'Secondary', 'Academy', 'Girls', 'Boys'])}",
            'school_type': s_type,
            'capacity': capacity,
            'latitude': lat,
            'longitude': lon,
            'min_entry_score': min_score,
            'resources_score': random.randint(1, 10) # 1-10 scale for resource availability
        })
    
    return pd.DataFrame(schools)

def generate_students(n_students=2000, schools_df=None):
    """
    Generates a DataFrame of students with scores, preferences, and demographics.
    """
    students = []
    
    center_lat, center_lon = -1.2921, 36.8219
    
    school_ids = schools_df['school_id'].tolist() if schools_df is not None else []

    for i in range(n_students):
        gender = np.random.choice(['Male', 'Female'])
        
        # Socioeconomic score (1-10), correlated slightly with performance for realism
        socioeconomic_status = np.random.randint(1, 11)
        
        # Performance (KCPE Marks out of 500)
        # Base score + random variation + slight boost for higher socioeconomic status
        base_score = np.random.normal(250, 60)
        score = min(max(int(base_score + (socioeconomic_status * 3)), 100), 500)
        
        # Disability
        disability = np.random.choice([0, 1], p=[0.98, 0.02])
        
        # Location
        lat = center_lat + np.random.normal(0, 0.5)
        lon = center_lon + np.random.normal(0, 0.5)

        # Preferences (Top 3 choices)
        choices = random.sample(school_ids, k=3) if school_ids else []
        
        students.append({
            'student_id': f'ST{i+10000}',
            'name': fake.name_male() if gender == 'Male' else fake.name_female(),
            'gender': gender,
            'score': score,
            'latitude': lat,
            'longitude': lon,
            'socioeconomic_status': socioeconomic_status,
            'disability': disability,
            'choice_1': choices[0] if len(choices) > 0 else None,
            'choice_2': choices[1] if len(choices) > 1 else None,
            'choice_3': choices[2] if len(choices) > 2 else None,
        })
        
    return pd.DataFrame(students)

if __name__ == "__main__":
    print("Generating synthetic data...")
    schools = generate_schools(50)
    students = generate_students(5000, schools)
    
    schools.to_csv('schools_data.csv', index=False)
    students.to_csv('students_data.csv', index=False)
    print(f"Generated {len(schools)} schools and {len(students)} students.")
