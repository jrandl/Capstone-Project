"""
LAPD Crime Dataset - Column Reference (28 Total Columns)
---------------------------------------------------------

This dataset contains detailed crime report records from the Los Angeles Police Department
(LAPD), covering incidents from 2020 to the present. Each record represents a reported
crime and includes information about the type, time, location, victim details, weapons
used, and investigation status.

Columns (in order):

1.  DR_NO (dr_no, Text):
    Division of Records Number – unique LAPD file number made up of a 2-digit year,
    area ID, and 5-digit serial number.

2.  Date Rptd (date_rptd, Floating Timestamp):
    The date the crime was reported to LAPD.

3.  DATE OCC (date_occ, Floating Timestamp):
    The date when the crime actually occurred.

4.  TIME OCC (time_occ, Text):
    Time of crime occurrence in 24-hour military time (e.g., 1345 = 1:45 PM).

5.  AREA (area, Text):
    Numeric LAPD division code (1–21) representing a community police station.

6.  AREA NAME (area_name, Text):
    Name of the LAPD geographic area/patrol division (e.g., "Wilshire", "Central").

7.  Rpt Dist No (rpt_dist_no, Text):
    Four-digit reporting district within the geographic area.

8.  Part 1-2 (part_1_2, Number):
    Indicates whether the crime is classified as a Part I (serious) or Part II offense.

9.  Crm Cd (crm_cd, Text):
    Primary crime code (same as Crm Cd 1).

10. Crm Cd Desc (crm_cd_desc, Text):
    Textual description of the primary crime (e.g., "BURGLARY", "ROBBERY").

11. Mocodes (mocodes, Text):
    Modus Operandi codes – identify suspect actions or criminal techniques.

12. Vict Age (vict_age, Text):
    Age of the victim (2-character numeric).

13. Vict Sex (vict_sex, Text):
    Victim's gender: M = Male, F = Female, X = Unknown.

14. Vict Descent (vict_descent, Text):
    Victim's descent code (e.g., B = Black, H = Hispanic, W = White, etc.).

15. Premis Cd (premis_cd, Number):
    Code indicating the type of premises where the incident occurred.

16. Premis Desc (premis_desc, Text):
    Description of the location/premises (e.g., STREET, RESTAURANT).

17. Weapon Used Cd (weapon_used_cd, Text):
    Code representing the weapon used (if applicable).

18. Weapon Desc (weapon_desc, Text):
    Textual description of the weapon (e.g., "HAND GUN", "KNIFE").

19. Status (status, Text):
    Investigation or resolution status code (e.g., IC = Initial Case).

20. Status Desc (status_desc, Text):
    Description of the case status (e.g., "Adult Arrest", "Invest Cont").

21. Crm Cd 1 (crm_cd_1, Text):
    Most serious crime code in the incident.

22. Crm Cd 2 (crm_cd_2, Text):
    Secondary crime code if multiple crimes occurred.

23. Crm Cd 3 (crm_cd_3, Text):
    Tertiary crime code (optional).

24. Crm Cd 4 (crm_cd_4, Text):
    Quaternary crime code (optional).

25. LOCATION (location, Text):
    Rounded address (to nearest hundred block) where the crime occurred.

26. Cross Street (cross_street, Text):
    Cross street near the location of the crime (optional/may be missing).

27. LAT (lat, Number):
    Latitude coordinate for geospatial analysis.

28. LON (lon, Number):
    Longitude coordinate for geospatial analysis.

Usage Notes:
------------
- Missing data may appear in victim demographics, coordinates, or status fields.
- Geospatial data enables mapping of high-risk zones.
- Categorical data (e.g., crime type, descent, area name) should be normalized for consistency.
- Crime codes may be used for classification or grouped into broader categories (violent, property, etc.).

"""
