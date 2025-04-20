# Understanding Crime in Los Angeles, California

### Author: Josiah Andrew Randleman  
Capstone Project for MS in Data Analytics, Northwest Missouri State University  
📍 GitHub Repository: [https://github.com/jrandl/Capstone-Project](https://github.com/jrandl/Capstone-Project)

---

## Project Overview

This project analyzes crime trends and patterns in Los Angeles, California using publicly available LAPD data. The primary goals were to:
- Identify high-risk areas based on crime frequency and severity
- Categorize crime types using descriptive analytics
- Build a predictive model to classify crime categories using incident-level data

---

## Datasets and Sources

### 1. **Crime Data (2020–2025)**
- Source: [Data.gov Crime Dataset](https://catalog.data.gov/dataset/crime-data-from-2020-to-present)
- Contains over 1 million records of reported crimes

### 2. **LAPD Geospatial Division Boundaries**
- Source: [Los Angeles GeoHub](https://geohub.lacity.org/datasets/lahub::lapd-divisions/about)
- Used for spatial analysis and choropleth maps

### 3. **Modus Operandi (MO) Codes**
- Source: [MO Codes Dictionary PDF](https://data.lacity.org/api/views/d5tf-ez2w/files/8957b3b1-771a-4686-8f19-281d23a11f1b?download=true&filename=MO_CODES_Numerical_20180627.pdf)
- Used to enrich crime reports with behavioral patterns

---


## Data Cleaning and Curation

The data cleaning pipeline:
- Filled over **5.5 million missing values**
- Standardized victim demographics
- Created **crime severity categories**
- Translated **MO codes into descriptive features**
- Exported cleaned data as `.csv` and `.pkl` files

Script: [`Data Cleaning and Curation Pipeline.py`](./Scripts/Data%20Cleaning%20and%20Curation%20Pipeline.py)

---

## Exploratory Data Analysis (EDA)

Performed using:
- Histograms, bar plots, and categorical counts
- Feature engineering: age groups, date features
- Crime frequency trends by area, day, time, and type

Script: [`EDA Pipeline.py`](./Scripts/EDA%20Pipeline.py)

Example Outputs:
- Victim Age Distribution
- Crime by Area and Day of Week
- Crime Category Distribution

Visuals saved to: `Output/Charts/`

---

## Geospatial Mapping

Mapped crimes by LAPD divisions and individual points using Folium:
- Interactive choropleth map (`Crime_Map_LAPD_Divisions.html`)
- Circle marker map (`Crime_Map_LA.html`)
- Heatmap (`Crime_Heatmap_LA.html`)

Script: [`map code.py`](./Scripts/map%20code.py)

---

## Predictive Modeling

Model: `RandomForestClassifier (n_estimators=100)`  
Target: `Crime_Category`

Process:
- Sampled 100,000 rows for efficiency
- One-hot encoded categorical features
- Split data 70/30 for training/testing
- Achieved **90.93% accuracy**

Evaluation Visuals:
- Confusion Matrix
- Normalized Confusion Matrix
- Classification Report Heatmap
- F1-Score by Crime Category
- Top 5 Feature Importances

Script: [`Predictive Analysis.py`](./Scripts/Predictive%20Analysis.py)

Model saved as: `Models/random_forest_model.pkl`

---

## Key Findings

- **Property Crime** and **Violent Crime** were the most predictable categories.
- **Sexual Offense** had lower recall, suggesting underrepresentation.
- Most predictive features: `Weapon Description`, `MO Codes`, `AREA NAME`.
- Highest crime rates were observed in the **Central** and **77th Street** divisions.

---


##  Final Report

The complete capstone report, including detailed methodology, results, limitations, and visualizations, is available at:

📄 [**Report/Josiah_Randleman_Capstone_Project_Report FINAL.pdf**](./Report/Josiah_Randleman_Capstone_Project_Report FINAL.pdf)

This document summarizes all findings and provides a comprehensive overview of the entire analysis pipeline from data collection to predictive modeling.

---


## Skills Demonstrated

- Data Engineering and Cleaning (pandas, regex, datetime parsing)
- Exploratory Data Analysis (matplotlib, seaborn)
- Spatial Visualization (Folium, GeoPandas)
- Machine Learning (Scikit-Learn Random Forest)
- Feature Engineering & Interpretation
- Report Writing and Documentation

---

## References

1. LAPD Crime Dataset: https://catalog.data.gov/dataset/crime-data-from-2020-to-present  
2. LAPD MO Code Dictionary: https://data.lacity.org/api/views/d5tf-ez2w/files/8957b3b1-771a-4686-8f19-281d23a11f1b?download=true&filename=MO_CODES_Numerical_20180627.pdf
3. LAPD Divisions Map: https://geohub.lacity.org/datasets/lahub::lapd-divisions/about  
4. Project Source Code: https://github.com/jrandl/Capstone-Project

---

📬 For questions or collaborations, contact:  
📧 jrandl516@gmail.com 


