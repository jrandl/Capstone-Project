# === Import Libraries ===
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import os

# === STEP 1: Load Your Crime Data ===
print("\n=== STEP 1: Load Crime Data ===")
crime_df = pd.read_pickle(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\crime_df_cleaned.pkl")
print(f"✅ Loaded crime data with {crime_df.shape[0]:,} rows.")

# === STEP 2: Load LAPD Division GeoJSON ===
print("\n=== STEP 2: Load LAPD Divisions GeoJSON ===")
divisions_gdf = gpd.read_file(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\LAPD Divisions\LAPD_Division_5922489107755548254.geojson")
print(f"✅ Loaded division GeoJSON with {divisions_gdf.shape[0]} divisions.")

# Confirm columns
print("\n=== Columns in divisions_gdf ===")
print(divisions_gdf.columns.tolist())

# === STEP 3: Prepare Crime Data ===
print("\n=== STEP 3: Prepare Crime Data ===")

# Make sure AREA is string
crime_df['AREA'] = crime_df['AREA'].astype(str)

# Build mapping from AREA to AREA NAME (from your crime data)
area_mapping = dict(zip(crime_df['AREA'], crime_df['AREA NAME']))

# Add clean Division Name
crime_df['Division_Name'] = crime_df['AREA'].map(area_mapping)

# Print divisions
unique_divisions = crime_df[['AREA', 'Division_Name']].drop_duplicates().sort_values('AREA')
print("\nUnique Divisions Found:")
for idx, row in unique_divisions.iterrows():
    print(f" • AREA {row['AREA']}: {row['Division_Name']}")

# Group by Division Name
crime_counts = crime_df['Division_Name'].value_counts().reset_index()
crime_counts.columns = ['Division_Name', 'Crime Count']

# === STEP 4: Prepare Divisions GeoData ===
print("\n=== STEP 4: Prepare Divisions GeoData ===")

# Standardize names
divisions_gdf['APREC'] = divisions_gdf['APREC'].astype(str).str.strip().str.lower()
crime_counts['Division_Name'] = crime_counts['Division_Name'].astype(str).str.strip().str.lower()

# Merge crime counts into division boundaries
merged_gdf = divisions_gdf.merge(crime_counts, left_on='APREC', right_on='Division_Name', how='left')

# Fill missing crime counts with 0
merged_gdf['Crime Count'] = merged_gdf['Crime Count'].fillna(0)

print("✅ Merged crime counts into division boundaries.")

# === STEP 5: Create Interactive Crime Map ===
print("\n=== STEP 5: Create Interactive Crime Map ===")

# Base map centered over LA
m = folium.Map(location=[34.0522, -118.2437], zoom_start=10, tiles='cartodbpositron')

# Choropleth layer
Choropleth(
    geo_data=merged_gdf,
    data=merged_gdf,
    columns=['APREC', 'Crime Count'],
    key_on='feature.properties.APREC',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Crime Count by LAPD Division'
).add_to(m)

# Hover tooltips
folium.GeoJson(
    merged_gdf,
    name="Divisions",
    tooltip=folium.GeoJsonTooltip(
        fields=['APREC', 'Crime Count'],
        aliases=['Division:', 'Crimes:'],
        localize=True,
        sticky=False
    )
).add_to(m)

print("✅ Interactive crime map created.")

# === STEP 6: Save Map to HTML ===
print("\n=== STEP 6: Save Map to HTML ===")

output_dir = r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output"
os.makedirs(output_dir, exist_ok=True)

map_path = os.path.join(output_dir, "Crime_Map_LAPD_Divisions.html")
m.save(map_path)

print(f"✅ Map saved to: {map_path}")

# Done!
print("\n🎉 All steps complete! Your interactive map is ready.")
