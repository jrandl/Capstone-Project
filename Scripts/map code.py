import pandas as pd
import os
import matplotlib
matplotlib.use('TkAgg')  # or 'QtAgg' or 'Agg'
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  # <-- add this to format the numbers
import seaborn as sns

# ------------------------ STEP 1: Load Pickle File ------------------------ #
print("\n=== STEP 1: Load Pickle File ===")
# Load the cleaned dataframe
crime_df = pd.read_pickle(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\crime_df_cleaned.pkl")
print("✅ DataFrame loaded from Pickle file.")

# -------------------------------------------
# Step 3: Sample the Data (to keep map fast)
# -------------------------------------------
import folium
from folium.plugins import HeatMap
# We'll sample 1000 crimes to avoid making the map too heavy
sample_crimes = crime_df[['LAT', 'LON', 'Crime_Category']].dropna().sample(1000, random_state=42)

# -------------------------------------------
# Step 4: Create a Basic LA Map
# -------------------------------------------
# Center of Los Angeles
la_location = [34.0522, -118.2437]

crime_map = folium.Map(location=la_location, zoom_start=11)

# -------------------------------------------
# Step 5: Add Crime Points to Map
# -------------------------------------------
for _, row in sample_crimes.iterrows():
    folium.CircleMarker(
        location=[row['LAT'], row['LON']],
        radius=2,
        color='red' if row['Crime_Category'] == 'Violent Crime' else 'blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(crime_map)

# -------------------------------------------
# Step 6: Save the Crime Map
# -------------------------------------------
crime_map_path = r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Crime_Map_LA.html"
crime_map.save(crime_map_path)
print(f"✅ Crime Map saved to: {crime_map_path}")

# -------------------------------------------
# Step 7: Create a Heatmap
# -------------------------------------------
crime_heatmap = folium.Map(location=la_location, zoom_start=11)

# Prepare data for HeatMap
heat_data = sample_crimes[['LAT', 'LON']].dropna().values.tolist()

HeatMap(heat_data).add_to(crime_heatmap)

# -------------------------------------------
# Step 8: Save the Heatmap
# -------------------------------------------
crime_heatmap_path = r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Crime_Heatmap_LA.html"
crime_heatmap.save(crime_heatmap_path)
print(f"✅ Crime Heatmap saved to: {crime_heatmap_path}")







