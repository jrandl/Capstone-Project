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

print("\n=== Dataset Overview ===")

# Print shape
rows, cols = crime_df.shape
print(f"\n➡️ The dataset contains {rows:,} rows and {cols:,} columns.")

# Print info (types and missing values overview)
print("\n➡️ Data Types and Non-Null Counts:")
crime_df.info()

# Print first few rows
print("\n➡️ First 5 Rows of the Dataset:")
print(crime_df.head())

# Print basic descriptive statistics
print("\n➡️ Descriptive Statistics (including all columns):")
with pd.option_context('display.max_columns', None):  # Show all columns without truncation
    print(crime_df.describe(include='all'))

# Print missing values
print("\n➡️ Missing Values per Column:")
missing_values = crime_df.isnull().sum()
missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

if not missing_values.empty:
    print(missing_values.apply(lambda x: f"{x:,} missing"))
else:
    print("✅ No missing values detected.")

print("\n=== Statistical Summary ===")

# -------------------- Numerical Features -------------------- #
print("\n➡️ Descriptive Statistics for Numerical Variables:")

# Select numerical columns only
numerical_cols = crime_df.select_dtypes(include=['number']).columns.tolist()

# If there are numerical columns
if numerical_cols:
    num_summary = crime_df[numerical_cols].describe()
    with pd.option_context('display.float_format', '{:,.2f}'.format):  # Format numbers nicely
        print(num_summary)
else:
    print("⚠️ No numerical columns found.")

# -------------------- Categorical Features -------------------- #
print("\n➡️ Value Counts for Categorical Variables:")

# Select categorical columns only
categorical_cols = crime_df.select_dtypes(include=['object', 'category']).columns.tolist()

# If there are categorical columns
if categorical_cols:
    for col in categorical_cols:
        print(f"\n🔹 {col} (Top 5 most frequent values):")
        value_counts = crime_df[col].value_counts(dropna=False).head(5)
        print(value_counts.apply(lambda x: f"{x:,} occurrences"))
else:
    print("⚠️ No categorical columns found.")

print("\n=== Feature Distributions ===")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Save directory
save_dir = r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts"
os.makedirs(save_dir, exist_ok=True)

print("\n=== Step 2: Feature Distributions for Key Variables ===")

# Function to save and show plots
def save_and_show_plot(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, filename))
    plt.show()

# ----------------- 1. DR_NO ----------------- #
print("\n➡️ DR_NO: No plot needed (unique identifier).")

# ----------------- 2. DATE OCC ----------------- #
print("\n➡️ DATE OCC: Distribution of crime occurrences over time.")
plt.figure(figsize=(10,5))
crime_df['DATE OCC'] = pd.to_datetime(crime_df['DATE OCC'], errors='coerce')  # ensure datetime
crime_df['DATE OCC'].dt.to_period('M').value_counts().sort_index().plot(kind='line')
plt.title('Number of Crimes Over Time (Date of Occurrence)')
plt.xlabel('Month')
plt.ylabel('Number of Crimes')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Date_Occurrence_Distribution.png")
plt.show()

# ----------------- 6. Crm Cd Desc ----------------- #
print("\n➡️ Crm Cd Desc: Top Crime Descriptions.")
plt.figure(figsize=(10,6))
order = crime_df['Crm Cd Desc'].value_counts().head(10).index
sns.countplot(data=crime_df, y='Crm Cd Desc', order=order)
plt.title('Top 10 Crime Descriptions')
plt.xlabel('Number of Crimes')
plt.ylabel('Crime Description')
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Crime_Description_Distribution.png")
plt.show()

# ----------------- 8. Vict Age ----------------- #
print("\n➡️ Vict Age: Distribution of Victim Ages.")
plt.figure(figsize=(8,5))
sns.histplot(crime_df['Vict Age'].dropna(), bins=30, kde=True)
plt.title('Distribution of Victim Ages')
plt.xlabel('Age')
plt.ylabel('Number of Victims')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Victim_Age_Distribution.png")
plt.show()

# ----------------- 9. Vict Age Group ----------------- #
print("\n➡️ Vict Age Group: Distribution.")
plt.figure(figsize=(8,6))
order = crime_df['Vict Age Group'].value_counts().index
sns.countplot(data=crime_df, x='Vict Age Group', order=order)
plt.title('Victim Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Number of Victims')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Victim_Age_Group_Distribution.png")
plt.show()

# ----------------- 10. Vict Sex ----------------- #
print("\n➡️ Vict Sex: Gender distribution of victims.")
plt.figure(figsize=(6,5))
order = crime_df['Vict Sex'].value_counts().index
sns.countplot(data=crime_df, x='Vict Sex', order=order)
plt.title('Victim Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Number of Victims')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Victim_Sex_Distribution.png")
plt.show()

# ------------------------ STEP 2: Univariate Analysis on Crime Category------------------------ #
print("\n=== STEP 2: Univariate Analysis on Crime Category ===")
plt.figure(figsize=(10,6))
sns.countplot(data=crime_df, x='Crime_Category', order=crime_df['Crime_Category'].value_counts().index)
plt.title('Overall Crime Category Distribution')
plt.xlabel('Crime Category')
plt.ylabel('Number of Crimes')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Crime_Category.png")
plt.show()


# ------------------------ STEP 2: Univariate Analysis Area Name------------------------ #
print("\n=== STEP 3: Univariate Analysis on Area Name ===")
# Top 5 Areas for Crime in LA
top_areas = crime_df['AREA NAME'].value_counts().head(5)

plt.figure(figsize=(8,6))
sns.barplot(x=top_areas.index, y=top_areas.values)  # <-- swap x and y
plt.title('Top 5 LAPD Areas by Number of Crimes')
plt.ylabel('Number of Crimes')
plt.xlabel('LAPD Area Name')
plt.xticks(rotation=45)  # Tilt x labels so they don't overlap
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Top_5_Areas.png")
plt.show()

# ------------------------ STEP 4: Univariate Analysis DayOfWeek------------------------ #
print("\n=== STEP 4: Univariate Analysis on DayOfWeek ===")
# Plot number of crimes per day of the week
crime_df['DayOfWeek'].value_counts().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Unknown'
]).plot(kind='bar', figsize=(10,6))
plt.title('Crimes by Day of the Week')
plt.xlabel('Day')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\DayOfWeek.png")
plt.show()

# ------------------------ STEP 5: Multivariate Analysis on Crime Categories Across Victim Age Groups------------------------ #
print("\n=== STEP 5: Multivariate Analysis on Crime Categories Across Victim Age Groups ===")
# Count plot of Age Group vs Crime Category
plt.figure(figsize=(10,6))
sns.countplot(x='Vict Age Group', hue='Crime_Category', data=crime_df)
plt.title('Crime Categories Across Victim Age Groups')
plt.xlabel('Victim Age Group')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=45)
plt.legend(title='Crime Category')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Crime_Categories_Across_Victim_Age_Groups.png")
plt.show()

# ------------------------ STEP 6: Bivariate Analysis: Area vs Crime Category (Bar Plot)------------------------ #
print("\n=== STEP 6: Bivariate Analysis: Area vs Crime Category ===")
plt.figure(figsize=(14,8))
sns.countplot(x='AREA NAME', hue='Crime_Category', data=crime_df,
              order=crime_df['AREA NAME'].value_counts().index[:10])  # Top 10 areas if you want to limit

plt.title('Crime Category Distribution Across LAPD Areas')
plt.xlabel('LAPD Area Name')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=45, ha='right')  # Tilt x-labels
plt.legend(title='Crime Category')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Crime_Category_AreaName.png")
plt.show()

print("\n=== STEP 7: Yearly Crime Count with Year-over-Year Variance ===")

# Ensure 'DATE OCC' is in datetime format
crime_df['DATE OCC'] = pd.to_datetime(crime_df['DATE OCC'], errors='coerce')

# Extract Year
crime_df['Year'] = crime_df['DATE OCC'].dt.year

# Group by Year
yearly_counts = crime_df['Year'].value_counts().sort_index()

# Calculate year-over-year percentage change
yearly_pct_change = yearly_counts.pct_change() * 100  # Multiply by 100 to get %

# Plot
fig, ax1 = plt.subplots(figsize=(12,7))

# Bar plot for number of crimes
color = 'tab:blue'
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Crimes', color=color)
bars = ax1.bar(yearly_counts.index, yearly_counts.values, color=color, alpha=0.7)
ax1.tick_params(axis='y', labelcolor=color)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: format(int(x), ',')))

# Instantiate a second y-axis that shares the same x-axis
ax2 = ax1.twinx()

# Line plot for % change
color = 'tab:red'
ax2.set_ylabel('Year-over-Year Change (%)', color=color)
line = ax2.plot(yearly_pct_change.index, yearly_pct_change.values, color=color, marker='o', linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))

# Title and layout
plt.title('Yearly Crime Counts and Year-over-Year Percentage Change')
fig.tight_layout()

# Save and show
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\Charts\Yearly_Crime_Variance.png")
plt.show()
