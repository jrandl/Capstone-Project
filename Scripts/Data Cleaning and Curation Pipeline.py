import pandas as pd
import os

# ------------------------ STEP 1: Load Datasets ------------------------ #
print("\n=== STEP 1: Load Datasets ===")

crime_df = pd.read_csv(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Dataset\Crime_Data_from_2020_to_Present.csv")
codes_df = pd.read_csv(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\MO Codes\Mo_Codes.csv")

print(f" - Loaded crime dataset with {len(crime_df):,} rows and {crime_df.shape[1]} columns")
print(f" - Loaded MO codes with {len(codes_df):,} entries")

codes_df['Code'] = codes_df['Code'].astype(str).str.zfill(4)
mo_code_mapping = dict(zip(codes_df['Code'], codes_df['Description']))

# ------------------------ STEP 2: Clean Missing Values ------------------------ #
print("\n=== STEP 2: Cleaning Missing and Blank Values ===")

missing_counts = crime_df.isna().sum()
missing_total = missing_counts.sum()
print(f" - Total missing values before fill: {missing_total:,}")
for col, count in missing_counts.items():
    if count > 0:
        print(f"   • {col}: {count:,} missing")

for col in crime_df.columns:
    if crime_df[col].dtype == 'object' or pd.api.types.is_string_dtype(crime_df[col]):
        crime_df[col] = crime_df[col].replace(r'^\s*$', pd.NA, regex=True)
        crime_df[col] = crime_df[col].fillna("Unknown")
    else:
        crime_df[col] = crime_df[col].fillna("Unknown").astype(str)

print(f" - All missing and blank values filled. Remaining NAs: {crime_df.isna().sum().sum()}")

# ------------------------ STEP 3: Drop Duplicates ------------------------ #
print("\n=== STEP 3: Removing Duplicate Records by DR_NO ===")

crime_df['DR_NO'] = crime_df['DR_NO'].astype(str)
before_dupes = len(crime_df)
crime_df.drop_duplicates(subset='DR_NO', inplace=True)
after_dupes = len(crime_df)

print(f" - Removed {before_dupes - after_dupes:,} duplicate records")

# ------------------------ STEP 4: Parse and Format Dates ------------------------ #
print("\n=== STEP 4: Parsing and Formatting Dates ===")

crime_df['DATE OCC'] = pd.to_datetime(crime_df['DATE OCC'], errors='coerce')
crime_df['Date Rptd'] = pd.to_datetime(crime_df['Date Rptd'], errors='coerce')

crime_df['DayOfWeek'] = crime_df['DATE OCC'].dt.day_name().fillna("Unknown")
crime_df['Month'] = crime_df['DATE OCC'].dt.strftime('%B').fillna("Unknown")

crime_df['DATE OCC'] = crime_df['DATE OCC'].dt.strftime('%m/%d/%Y').fillna("Unknown")
crime_df['Date Rptd'] = crime_df['Date Rptd'].dt.strftime('%m/%d/%Y').fillna("Unknown")

print(" - Dates converted to MM/DD/YYYY format")
print(" - Weekday and month extracted as text")
print(crime_df[['Date Rptd', 'DATE OCC', 'DayOfWeek', 'Month']].head(10))

# ------------------------ STEP 5: Convert TIME OCC ------------------------ #
print("\n=== STEP 5: Converting TIME OCC to 12-Hour Format ===")

def military_to_am_pm(military_str):
    try:
        military_str = str(military_str).zfill(4)
        hour = int(military_str[:2])
        minute = int(military_str[2:])
        return pd.Timestamp(f'{hour:02}:{minute:02}').strftime('%I:%M %p')
    except:
        return "Unknown"

crime_df['TIME OCC'] = crime_df['TIME OCC'].apply(military_to_am_pm)
print(" - Converted TIME OCC to 12-hour format")
print(crime_df[['TIME OCC']].head())

# ------------------------ STEP 6: Clean Demographics ------------------------ #
print("\n=== STEP 6: Cleaning Victim Age, Sex, and Descent ===")

crime_df['Vict Age'] = crime_df['Vict Age'].astype(str)
crime_df['Vict Age'] = crime_df['Vict Age'].replace(['0', 0], 'Unknown')

crime_df['Vict Sex'] = crime_df['Vict Sex'].replace({'': 'Unknown', 'X': 'Unknown', 'M': 'Male', 'F': 'Female'})

descent_mapping = {
    'A': 'Other Asian', 'B': 'Black', 'C': 'Chinese', 'D': 'Cambodian',
    'F': 'Filipino', 'G': 'Guamanian', 'H': 'Hispanic/Latin/Mexican',
    'I': 'American Indian/Alaskan Native', 'J': 'Japanese', 'K': 'Korean',
    'L': 'Laotian', 'O': 'Other', 'P': 'Pacific Islander', 'S': 'Samoan',
    'U': 'Hawaiian', 'V': 'Vietnamese', 'W': 'White', 'X': 'Unknown',
    'Z': 'Asian Indian'
}
crime_df['Vict Descent'] = crime_df['Vict Descent'].map(descent_mapping).fillna('Unknown')

mask = (crime_df['Vict Sex'] == 'Unknown') & (crime_df['Vict Descent'] == 'Unknown')
crime_df.loc[mask, 'Vict Age'] = 'Unknown'

age_bins = [0, 12, 18, 25, 35, 50, 65, 100, 150]
age_labels = ['Child (0-12)', 'Teen (13-18)', 'Young Adult (19-25)', 'Adult (26-35)',
              'Middle Age (36-50)', 'Senior (51-65)', 'Elderly (66-100)', 'Super Elderly (100+)']

crime_df['Vict Age Group'] = pd.to_numeric(crime_df['Vict Age'], errors='coerce')
crime_df['Vict Age Group'] = pd.cut(crime_df['Vict Age Group'], bins=age_bins, labels=age_labels)
crime_df['Vict Age Group'] = crime_df['Vict Age Group'].cat.add_categories(['Unknown']).fillna('Unknown')

print("\n=== Victim Age Group Distribution ===")
age_group_counts = crime_df['Vict Age Group'].value_counts().sort_index()
for group, count in age_group_counts.items():
    print(f" • {group}: {count:,} victims")


# ------------------------ STEP 7: Expanding MO Codes into Descriptions ------------------------ #
print("\n=== STEP 7: Expanding MO Codes into Descriptions ===")

def expand_mocodes_to_descriptions(mocode_string):
    if pd.isna(mocode_string) or mocode_string.strip() == "" or mocode_string.strip().lower() == "unknown":
        return ["None"]
    code_list = mocode_string.strip().split()
    return [mo_code_mapping.get(code.zfill(4), "None") for code in code_list]

crime_df["MO_Descriptions_List"] = crime_df["Mocodes"].apply(expand_mocodes_to_descriptions)
max_mo_codes = crime_df["MO_Descriptions_List"].apply(len).max()
mo_desc_columns = [f"MO_Desc_{i+1}" for i in range(max_mo_codes)]

mo_desc_df = pd.DataFrame(crime_df["MO_Descriptions_List"].to_list(), columns=mo_desc_columns)
mo_desc_df.fillna("None", inplace=True)

crime_df = pd.concat([crime_df, mo_desc_df], axis=1)
crime_df.drop(columns=["MO_Descriptions_List"], inplace=True)

print(f" - Total MO Description columns created: {len(mo_desc_columns)}")
print(f" - Sample MO Descriptions:")
print(crime_df[["Mocodes"] + mo_desc_columns].head())

# ------------------------ STEP 8: Crime Category Mapping ------------------------ #
print("\n=== STEP 8: Creating Crime Severity Categories ===")
def print_unique_crime_descriptions(df):
    print("\n=== Unique Values in 'Crm Cd Desc' ===")
    value_counts = df['Crm Cd Desc'].value_counts(dropna=False).sort_values(ascending=False)
    print(f" - Total Unique Descriptions: {len(value_counts)}\n")
    for desc, count in value_counts.items():
        print(f" • {desc}: {count:,} occurrences")

print_unique_crime_descriptions(crime_df)

crime_category_mapping = {
    # Violent Crimes
    "BATTERY - SIMPLE ASSAULT": "Violent Crime",
    "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT": "Violent Crime",
    "INTIMATE PARTNER - SIMPLE ASSAULT": "Violent Crime",
    "INTIMATE PARTNER - AGGRAVATED ASSAULT": "Violent Crime",
    "BATTERY POLICE (SIMPLE)": "Violent Crime",
    "BATTERY WITH SEXUAL CONTACT": "Violent Crime",
    "ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER": "Violent Crime",
    "CRIMINAL THREATS - NO WEAPON DISPLAYED": "Violent Crime",
    "CRIMINAL HOMICIDE": "Violent Crime",
    "ATTEMPTED ROBBERY": "Violent Crime",
    "ROBBERY": "Violent Crime",
    "OTHER ASSAULT": "Violent Crime",
    "KIDNAPPING": "Violent Crime",
    "KIDNAPPING - GRAND ATTEMPT": "Violent Crime",
    "CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT": "Violent Crime",
    "CHILD ABUSE (PHYSICAL) - AGGRAVATED ASSAULT": "Violent Crime",
    "CRM AGNST CHLD (13 OR UNDER) (14-15 & SUSP 10 YRS OLDER)": "Violent Crime",
    "RESISTING ARREST": "Violent Crime",

    # Property Crimes
    "VEHICLE - STOLEN": "Property Crime",
    "BURGLARY FROM VEHICLE": "Property Crime",
    "BURGLARY": "Property Crime",
    "THEFT PLAIN - PETTY ($950 & UNDER)": "Property Crime",
    "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)": "Property Crime",
    "THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)": "Property Crime",
    "THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD": "Property Crime",
    "SHOPLIFTING - PETTY THEFT ($950 & UNDER)": "Property Crime",
    "SHOPLIFTING-GRAND THEFT ($950.01 & OVER)": "Property Crime",
    "BURGLARY, ATTEMPTED": "Property Crime",
    "VEHICLE - ATTEMPT STOLEN": "Property Crime",
    "BIKE - STOLEN": "Property Crime",
    "BIKE - ATTEMPTED STOLEN": "Property Crime",
    "THEFT, PERSON": "Property Crime",
    "BURGLARY FROM VEHICLE, ATTEMPTED": "Property Crime",
    "THEFT FROM MOTOR VEHICLE - ATTEMPT": "Property Crime",
    "BOAT - STOLEN": "Property Crime",
    "PICKPOCKET": "Property Crime",
    "PICKPOCKET, ATTEMPT": "Property Crime",
    "PURSE SNATCHING": "Property Crime",
    "PURSE SNATCHING - ATTEMPT": "Property Crime",
    "TILL TAP - PETTY ($950 & UNDER)": "Property Crime",
    "TILL TAP - GRAND THEFT ($950.01 & OVER)": "Property Crime",
    "THEFT, COIN MACHINE - PETTY ($950 & UNDER)": "Property Crime",
    "THEFT, COIN MACHINE - GRAND ($950.01 & OVER)": "Property Crime",
    "THEFT, COIN MACHINE - ATTEMPT": "Property Crime",
    "THEFT PLAIN - ATTEMPT": "Property Crime",
    "SHOPLIFTING - ATTEMPT": "Property Crime",
    "EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)": "Property Crime",
    "EMBEZZLEMENT, PETTY THEFT ($950 & UNDER)": "Property Crime",
    "DRIVING WITHOUT OWNER CONSENT (DWOC)": "Property Crime",
    "ARSON": "Property Crime",

    # Public Order Crimes
    "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)": "Public Order Crime",
    "VANDALISM - MISDEAMEANOR ($399 OR UNDER)": "Public Order Crime",
    "TRESPASSING": "Public Order Crime",
    "BRANDISH WEAPON": "Public Order Crime",
    "DISTURBING THE PEACE": "Public Order Crime",
    "DISCHARGE FIREARMS/SHOTS FIRED": "Public Order Crime",
    "SHOTS FIRED AT INHABITED DWELLING": "Public Order Crime",
    "SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT": "Public Order Crime",
    "THROWING OBJECT AT MOVING VEHICLE": "Public Order Crime",
    "ILLEGAL DUMPING": "Public Order Crime",
    "BLOCKING DOOR INDUCTION CENTER": "Public Order Crime",
    "FAILURE TO YIELD": "Public Order Crime",
    "FAILURE TO DISPERSE": "Public Order Crime",
    "PEEPING TOM": "Public Order Crime",
    "PROWLER": "Public Order Crime",
    "DISRUPT SCHOOL": "Public Order Crime",
    "WEAPONS POSSESSION/BOMBING": "Public Order Crime",
    "FIREARMS EMERGENCY PROTECTIVE ORDER (FIREARMS EPO)": "Public Order Crime",
    "FIREARMS RESTRAINING ORDER (FIREARMS RO)": "Public Order Crime",

    # Sexual Offenses
    "RAPE, FORCIBLE": "Sexual Offense",
    "RAPE, ATTEMPTED": "Sexual Offense",
    "ORAL COPULATION": "Sexual Offense",
    "SODOMY/SEXUAL CONTACT B/W PENIS OF ONE PERS TO ANUS OTH": "Sexual Offense",
    "SEXUAL PENETRATION W/FOREIGN OBJECT": "Sexual Offense",
    "SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ": "Sexual Offense",
    "LEWD/LASCIVIOUS ACTS WITH CHILD": "Sexual Offense",
    "LEWD CONDUCT": "Sexual Offense",
    "CHILD ANNOYING (17YRS & UNDER)": "Sexual Offense",
    "INDECENT EXPOSURE": "Sexual Offense",
    "INCEST (SEXUAL ACTS BETWEEN BLOOD RELATIVES)": "Sexual Offense",
    "BEASTIALITY, CRIME AGAINST NATURE SEXUAL ASSLT WITH ANIM": "Sexual Offense",

    # White Collar Crimes
    "THEFT OF IDENTITY": "White Collar Crime",
    "CREDIT CARDS, FRAUD USE ($950.01 & OVER)": "White Collar Crime",
    "CREDIT CARDS, FRAUD USE ($950 & UNDER": "White Collar Crime",
    "BUNCO, GRAND THEFT": "White Collar Crime",
    "BUNCO, PETTY THEFT": "White Collar Crime",
    "BUNCO, ATTEMPT": "White Collar Crime",
    "DOCUMENT FORGERY / STOLEN FELONY": "White Collar Crime",
    "DOCUMENT WORTHLESS ($200.01 & OVER)": "White Collar Crime",
    "DOCUMENT WORTHLESS ($200 & UNDER)": "White Collar Crime",
    "DISHONEST EMPLOYEE - GRAND THEFT": "White Collar Crime",
    "DISHONEST EMPLOYEE - PETTY THEFT": "White Collar Crime",
    "DISHONEST EMPLOYEE ATTEMPTED THEFT": "White Collar Crime",
    "DEFRAUDING INNKEEPER/THEFT OF SERVICES, $950 & UNDER": "White Collar Crime",
    "DEFRAUDING INNKEEPER/THEFT OF SERVICES, OVER $950.01": "White Collar Crime",
    "EXTORTION": "White Collar Crime",
    "EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)": "White Collar Crime",
    "COUNTERFEIT": "White Collar Crime",
    "FORGERY": "White Collar Crime",
    "UNAUTHORIZED COMPUTER ACCESS": "White Collar Crime",
    "GRAND THEFT / INSURANCE FRAUD": "White Collar Crime",

    # Other / Miscellaneous
    "OTHER MISCELLANEOUS CRIME": "Other",
    "VIOLATION OF RESTRAINING ORDER": "Other",
    "VIOLATION OF TEMPORARY RESTRAINING ORDER": "Other",
    "VIOLATION OF COURT ORDER": "Other",
    "SEX OFFENDER REGISTRANT OUT OF COMPLIANCE": "Other",
    "CHILD NEGLECT (SEE 300 W.I.C.)": "Other",
    "CHILD STEALING": "Other",
    "CHILD ABANDONMENT": "Other",
    "CHILD PORNOGRAPHY": "Other",
    "FALSE IMPRISONMENT": "Other",
    "FALSE POLICE REPORT": "Other",
    "CONTEMPT OF COURT": "Other",
    "THREATENING PHONE CALLS/LETTERS": "Other",
    "LYNCHING": "Other",
    "LYNCHING - ATTEMPTED": "Other",
    "HUMAN TRAFFICKING - COMMERCIAL SEX ACTS": "Other",
    "HUMAN TRAFFICKING - INVOLUNTARY SERVITUDE": "Other",
    "PANDERING": "Other",
    "PIMPING": "Other",
    "CONSPIRACY": "Other",
    "CONTRIBUTING": "Other",
    "BIGAMY": "Other",
    "BRIBERY": "Other",
    "TRAIN WRECKING": "Other",
    "DRUGS, TO A MINOR": "Other",
    "REPLICA FIREARMS(SALE,DISPLAY,MANUFACTURE OR DISTRIBUTE)": "Other",
    "SEX OFFENDER REGISTRANT OUT OF COMPLIANCE": "Other",
    "DRUNK ROLL": "Other",
    "DRUNK ROLL - ATTEMPT": "Other"
}

# Apply mapping
crime_df['Crime_Category'] = crime_df['Crm Cd Desc'].map(crime_category_mapping).fillna("Other")

# Summary
print("\n=== Category Counts ===")
category_counts = crime_df['Crime_Category'].value_counts()
for category, count in category_counts.items():
    print(f" • {category:<20}: {count:,}")


# ------------------------ STEP 9: Export to CSV ------------------------ #
print("\n=== STEP 9: Exporting Cleaned Data ===")

output_dir = r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output"
os.makedirs(output_dir, exist_ok=True)

output_df = crime_df.head(5000)
output_path = os.path.join(output_dir, "Output.csv")
output_df.to_csv(output_path, index=False)

print(f"\n✅ Exported first 5,000 records to:\n{output_path}")
print(f" - Final dataset shape: {crime_df.shape}")
print(" - Column Preview:", crime_df.columns.tolist())


# ------------------------ STEP 10: Export to Pickle ------------------------ #
print("\n=== STEP 10: Export to Pickle ===")
# Save the cleaned dataframe
crime_df.to_pickle(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\crime_df_cleaned.pkl")
print("✅ DataFrame saved as Pickle file.")


