# AI-Optimized Student Placement System (Kenya CBC Grade 10)
An AI-based prototype designed to optimize the placement of Grade 10 students into senior secondary schools in Kenya under the Competency-Based Curriculum (CBC). This system addresses challenges such as overcrowding, system glitches, and inequities by leveraging machine learning and multi-criteria optimization.
## 🎯 Project Objective
The goal of this project is to create a fair, transparent, and efficient student-school matching system that:
- **Maximizes Student Satisfaction**: Prioritizes student choices and pathways (STEM, Arts, Vocational).
- **Reduces Travel Burden**: Optimizes for geographic proximity.
- **Ensures Equity**: Actively audits and mitigates bias based on gender and socioeconomic status (SES).
- **Prevents Overcrowding**: Dynamically manages school capacities.
- **Forecasts Demand**: Uses predictive analytics to help policy makers allocate resources proactively.
## 🚀 Key Features
- **AI-Optimized Matching**: A greedy optimization algorithm implementing a multi-criteria utility function.
- **Predictive Analytics**: Time-series forecasting for future enrollment trends.
- **Fairness & Bias Auditing**: Built-in metrics (Gender Parity Ratio, SES Disparity) to ensure equitable outcomes.
- **Interactive Dashboard**: A Streamlit interface for map visualizations, analytics reporting, and data management.
- **Synthetic Data Engine**: Generates realistic, anonymized student and school profiles for simulation.
## 🛠️ Technology Stack
- **Language**: Python 3.x
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Science**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning**: [Scikit-learn](https://scikit-learn.org/)
- **Visualization**: [Folium](https://python-visualization.github.io/folium/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
- **Data Generation**: [Faker](https://faker.readthedocs.io/)
## 📂 Project Structure
```text
student_placement_system/
├── app/
│   └── main.py            # Streamlit dashboard entry point
├── data/
│   ├── generator.py       # Synthetic data generation logic
│   └── processing.py      # Data loading and preprocessing
├── models/
│   ├── matching.py        # Core assignment & optimization engine
│   ├── prediction.py      # Enrollment forecasting model
│   └── fairness.py        # Bias detection & auditing logic
├── tests/
│   └── test_flow.py       # Automated integration tests
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```
## ⚙️ Installation & Usage
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/student-placement-ai.git
   cd student-placement-ai
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r student_placement_system/requirements.txt
   ```
3. **Run the Dashboard**:
   ```bash
   streamlit run student_placement_system/app/main.py
   ```
4. **Verify the System**:
   ```bash
   python student_placement_system/tests/test_flow.py
   ```
## ⚖️ Ethical Safeguards
This system is designed as a Decision Support System (DSS). It includes:
- **Anonymization**: Synthetic data ensures no real PII is used in this prototype.
- **Fairness Metrics**: Explicit reporting on disparate impact to inform human oversight.
- **Human-in-the-loop**: Final placement review capability before commitment.
## 📜 License
Distributed under the MIT License. See `LICENSE` for more information
