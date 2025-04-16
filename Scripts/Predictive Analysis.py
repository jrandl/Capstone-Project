# ================================
# STEP 1: Load Libraries
# ================================
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ================================
# STEP 1: Load Pickle File
# ================================
print("\n=== STEP 1: Load Pickle File ===")

# Load the cleaned dataframe
crime_df = pd.read_pickle(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Output\crime_df_cleaned.pkl")
print("DataFrame loaded from Pickle file.")
print(f"Original Dataset Shape: {crime_df.shape}")

# ================================
# STEP 2: Sample 100,000 Rows
# ================================
print("\n=== STEP 2: Sample 100,000 Rows ===")

# Randomly sample 100,000 rows
crime_df_sampled = crime_df.sample(n=100000, random_state=42)
print(f"Sampled Dataset Shape: {crime_df_sampled.shape}")

# ================================
# STEP 3: Feature and Target Selection
# ================================
print("\n=== STEP 3: Feature and Target Selection ===")

features = [
    'TIME OCC', 'AREA NAME', 'Vict Age', 'Vict Sex', 'Vict Descent', 'Premis Desc', 'Weapon Desc',
    'DayOfWeek', 'Month', 'MO_Desc_1', 'MO_Desc_2', 'MO_Desc_3', 'MO_Desc_4', 'MO_Desc_5', 'MO_Desc_6',
    'MO_Desc_7', 'MO_Desc_8', 'MO_Desc_9', 'MO_Desc_10'
]

target = 'Crime_Category'

# Features (X) and Target (y)
X = pd.get_dummies(crime_df_sampled[features])

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(crime_df_sampled[target])

print(f"Features and target prepared. Feature matrix shape: {X.shape}")

# ================================
# STEP 4: Train-Test Split
# ================================
print("\n=== STEP 4: Train-Test Split ===")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"Data split into training set {X_train.shape} and testing set {X_test.shape}")

# ================================
# STEP 5: Model Training
# ================================
print("\n=== STEP 5: Model Training ===")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

print("Random Forest model trained.")

# ================================
# STEP 6: Model Prediction
# ================================
print("\n=== STEP 6: Model Prediction ===")

y_pred = rf_model.predict(X_test)

# ================================
# STEP 7: Model Evaluation
# ================================
print("\n=== STEP 7: Model Evaluation ===")

# Classification Report
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n=== Accuracy: {accuracy*100:.2f}% ===")

# Confusion Matrix
print("\n=== Confusion Matrix ===")
conf_matrix = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10,7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\confusion_matrix.png")
plt.close()
print("Confusion Matrix plot saved as 'confusion_matrix.png'")

# Generate classification report as a dictionary
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)

# Convert to DataFrame
report_df = pd.DataFrame(report).transpose()

# Plot heatmap (only precision, recall, and f1-score)
plt.figure(figsize=(10, 6))
sns.heatmap(report_df.iloc[:-1, :3], annot=True, cmap='YlGnBu')
plt.title('Classification Report Heatmap')
plt.xlabel('Metrics')
plt.ylabel('Crime Categories')
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\classification_report_heatmap.png")
plt.close()
print("Classification Report Heatmap saved as 'classification_report_heatmap.png'")

# Normalize the confusion matrix
conf_matrix_norm = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]

# Plot normalized confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix_norm, annot=True, fmt=".2f", cmap='Blues',
            xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Normalized Confusion Matrix')
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\normalized_confusion_matrix.png")
plt.close()
print("Normalized Confusion Matrix plot saved as 'normalized_confusion_matrix.png'")

# ================================
# STEP 9: Other Charts
# ================================
print("\n=== STEP 9: Create More Charts ===")
# F1-score bar plot
f1_scores = report_df.loc[label_encoder.classes_, 'f1-score']
f1_scores.sort_values().plot(kind='barh', figsize=(10,6), title='F1-Score by Crime Category')
plt.xlabel('F1-Score')
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\f1_score_by_category.png")
plt.close()


importances = rf_model.feature_importances_
feat_names = X.columns
feat_importance_df = pd.Series(importances, index=feat_names).sort_values(ascending=False).head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x=feat_importance_df, y=feat_importance_df.index)
plt.title('Top 5 Feature Importances in Crime Prediction')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\feature_importance.png")
plt.close()


area_counts = crime_df_sampled['AREA NAME'].value_counts()
area_counts.plot(kind='barh', figsize=(10,6), title='Crime Reports by LAPD Area')
plt.xlabel('Number of Incidents')
plt.tight_layout()
plt.savefig(r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\crime_by_area.png.png")
plt.close()


# ================================
# STEP 10: Save Model
# ================================
import joblib

print("\n=== STEP 10: Save Trained Model ===")

# Save the Random Forest model
model_save_path = r"C:\Users\Josiah Randleman\Documents\_Capstone Project\Models\random_forest_model.pkl"
joblib.dump(rf_model, model_save_path)

print(f"Random Forest model saved as 'random_forest_model.pkl'")



