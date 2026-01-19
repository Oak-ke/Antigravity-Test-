
import pandas as pd
import os
from .generator import generate_schools, generate_students

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
SCHOOLS_FILE = os.path.join(DATA_DIR, 'schools_data.csv')
STUDENTS_FILE = os.path.join(DATA_DIR, 'students_data.csv')

def load_data(regenerate=False):
    """
    Loads students and schools data. Generates it if missing or requested.
    """
    if regenerate or not os.path.exists(SCHOOLS_FILE) or not os.path.exists(STUDENTS_FILE):
        print("Generating new data...")
        schools = generate_schools(50)
        students = generate_students(5000, schools) # 100 students per school avg is too high for 50 schools with cap ~300? 
        # Wait, 50 schools * ~300 cap = 15000 capacity. 5000 students is fine.
        
        schools.to_csv(SCHOOLS_FILE, index=False)
        students.to_csv(STUDENTS_FILE, index=False)
    else:
        print("Loading existing data...")
        schools = pd.read_csv(SCHOOLS_FILE)
        students = pd.read_csv(STUDENTS_FILE)
        
    return students, schools
