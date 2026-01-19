
import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.processing import load_data
from models.matching import run_matching
from models.prediction import predict_enrollment
from models.fairness import calculate_bias_metrics

st.set_page_config(page_title="AI Student Placement System", layout="wide")

st.title("🎓 AI-Optimized Student Placement System")
st.markdown("### Optimizing Grade 10 Placements under CBC")

# Sidebar
st.sidebar.header("Control Panel")
regenerate = st.sidebar.button("🔄 Regenerate Synthetic Data")

# Load Data
if 'students_raw' not in st.session_state or regenerate:
    with st.spinner("Loading/Generating Data..."):
        students, schools = load_data(regenerate=regenerate)
        st.session_state['students_raw'] = students
        st.session_state['schools'] = schools
        # Reset placement
        if 'placed_students' in st.session_state:
            del st.session_state['placed_students']
        st.success("Data Loaded!")

students = st.session_state.get('students_raw')
schools = st.session_state.get('schools')

if students is not None:
    st.sidebar.markdown(f"**Total Students:** {len(students)}")
    st.sidebar.markdown(f"**Total Schools:** {len(schools)}")

# Main Actions
if st.sidebar.button("🚀 Run AI Placement"):
    with st.spinner("Running Optimization Algorithms..."):
        placed_df = run_matching(students, schools)
        st.session_state['placed_students'] = placed_df
        st.sidebar.success("Placement Complete!")

# Dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview & Maps", "⚖️ Fairness Audit", "🔮 Predictive Analytics", "📄 Data View"])

if 'placed_students' in st.session_state:
    placed_df = st.session_state['placed_students']
    merged_df = placed_df.merge(schools, left_on='assigned_school', right_on='school_id', suffixes=('_student', '_school'))
    
    with tab1:
        st.subheader("Placement Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Placement Rate", "100%") # We force placement in this prototype
        avg_score = placed_df['match_score'].mean()
        col2.metric("Avg. Match Utility", f"{avg_score:.2f}")
        
        # Map
        st.markdown("### 🗺️ Geographic Distribution")
        # Center map on Mean
        m = folium.Map(location=[merged_df['latitude_school'].mean(), merged_df['longitude_school'].mean()], zoom_start=10)
        
        # Plot schools
        for _, row in schools.iterrows():
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=f"{row['school_name']} ({row['school_type']})\nCap: {row['capacity']}",
                icon=folium.Icon(color="blue", icon="university", prefix='fa')
            ).add_to(m)
            
        # Plot a sample of student lines to schools (too many for all)
        sample_assignments = merged_df.sample(min(100, len(merged_df)))
        for _, row in sample_assignments.iterrows():
            folium.PolyLine(
                [[row['latitude_student'], row['longitude_student']], 
                 [row['latitude_school'], row['longitude_school']]],
                color="red", weight=1, opacity=0.5
            ).add_to(m)
            
        st_folium(m, width=800, height=500)
        
    with tab2:
        st.subheader("Equity & Bias Detection")
        metrics, _ = calculate_bias_metrics(placed_df, schools)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gender Parity Ratio (Target: 1.0)", f"{metrics['gender_parity_ratio']:.2f}", 
                  delta_color="normal" if 0.9 < metrics['gender_parity_ratio'] < 1.1 else "inverse")
        
        c2.metric("SES Disparity (Low/High Access)", f"{metrics['ses_disparity']:.2f}",
                   help="Ratio of Low SES students in High Quality schools vs High SES students")
        
        c3.metric("Avg Travel Distance (Deg)", f"{metrics['avg_displacement']:.4f}")
        
        st.info("ℹ️ SES Disparity < 0.8 indicates potential inequality in access to high-quality schools for lower income students.")

    with tab3:
        st.subheader("Enrollment Trends & Predictions")
        preds = predict_enrollment()
        
        fig, ax = plt.subplots()
        ax.plot(preds['Year'], preds['Predicted_Enrollment'], marker='o', linestyle='--')
        ax.set_title("Projected Grade 10 Enrollment Demand")
        ax.set_ylabel("Students")
        st.pyplot(fig)
        
        st.markdown("**Strategic Insight:**")
        if preds['Predicted_Enrollment'].iloc[-1] > preds['Predicted_Enrollment'].iloc[0]:
            st.warning(f"Enrollment is projected to rise by {preds['Predicted_Enrollment'].iloc[-1] - preds['Predicted_Enrollment'].iloc[0]} students. Infrastructure expansion recommended.")
            
    with tab4:
        st.dataframe(placed_df[['student_id', 'gender', 'score', 'socioeconomic_status', 'assigned_school', 'match_score']])

else:
    st.info("Please load data and run the placement algorithm.")
