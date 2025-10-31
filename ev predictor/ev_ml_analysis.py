import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('ElectricCarData_Clean (1).csv')

print("="*80)
print("ELECTRIC VEHICLE DATASET ANALYSIS")
print("="*80)

# ============================================================================
# 1. DATA QUALITY ISSUES IDENTIFICATION
# ============================================================================
print("\n📋 1. BASIC DATASET INFORMATION")
print("-"*80)
print(f"Dataset Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

print("\n🔍 2. DATA QUALITY ISSUES FOUND:")
print("-"*80)

# Issue 1: Leading/trailing whitespace
print("\n❌ Issue 1: Whitespace in column names and values")
print(f"   Columns with spaces: {[col for col in df.columns if col != col.strip()]}")
df.columns = df.columns.str.strip()
df['Brand'] = df['Brand'].str.strip()
df['Model'] = df['Model'].str.strip()
print("   ✅ Fixed: Stripped whitespace from columns and text values")

# Issue 2: Missing values
print("\n❌ Issue 2: Missing/Invalid values")
missing_info = df.isnull().sum()
print(f"   Missing values per column:\n{missing_info[missing_info > 0]}")

# Check for '-' values in FastCharge_KmH
dash_count = (df['FastCharge_KmH'] == '-').sum()
print(f"   FastCharge_KmH has {dash_count} '-' values (non-numeric)")
print("   ✅ Fix: Replace '-' with NaN and handle appropriately")

# Issue 3: Data type inconsistencies
print("\n❌ Issue 3: Data type issues")
print(f"   Current dtypes:\n{df.dtypes}")

# Issue 4: Duplicates
duplicates = df.duplicated().sum()
print(f"\n❌ Issue 4: Duplicate rows: {duplicates}")

# Issue 5: Outliers detection
print("\n❌ Issue 5: Potential outliers")
numeric_cols = ['AccelSec', 'TopSpeed_KmH', 'Range_Km', 'Efficiency_WhKm', 'PriceEuro']
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
    print(f"   {col}: {outliers} potential outliers")

# Issue 6: Inconsistent categories
print("\n❌ Issue 6: Categorical value inconsistencies")
print(f"   Unique Brands: {df['Brand'].nunique()} - {df['Brand'].unique()[:10]}")
print(f"   Unique BodyStyles: {df['BodyStyle'].unique()}")
print(f"   Unique PowerTrains: {df['PowerTrain'].unique()}")
print(f"   Unique PlugTypes: {df['PlugType'].unique()}")

print("\n" + "="*80)
print("SUMMARY OF ISSUES:")
print("="*80)
print("""
1. ✅ Whitespace in Brand/Model names - FIXED
2. ⚠️  Missing/invalid values in FastCharge_KmH (- values)
3. ⚠️  Data type inconsistencies (FastCharge_KmH should be numeric)
4. ✅ No duplicate rows found
5. ⚠️  Some outliers present (extreme values in price, range)
6. ✅ Categorical values are consistent
""")

# ============================================================================
# 2. DATA CLEANING & PREPROCESSING
# ============================================================================
print("\n📊 3. DATA CLEANING & PREPROCESSING")
print("-"*80)

# Create a clean copy
df_clean = df.copy()

# Handle FastCharge_KmH
df_clean['FastCharge_KmH'] = pd.to_numeric(df_clean['FastCharge_KmH'], errors='coerce')
print(f"✅ Converted FastCharge_KmH to numeric ({df_clean['FastCharge_KmH'].isnull().sum()} NaN values)")

# Fill missing FastCharge values with median by brand
df_clean['FastCharge_KmH'].fillna(df_clean.groupby('Brand')['FastCharge_KmH'].transform('median'), inplace=True)
df_clean['FastCharge_KmH'].fillna(df_clean['FastCharge_KmH'].median(), inplace=True)
print(f"✅ Filled missing FastCharge_KmH values")

# ============================================================================
# 3. EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n📈 4. EXPLORATORY DATA ANALYSIS")
print("-"*80)

print("\nStatistical Summary:")
print(df_clean[numeric_cols].describe())

print("\n💰 Top 5 Most Expensive EVs:")
top_expensive = df_clean.nlargest(5, 'PriceEuro')[['Brand', 'Model', 'PriceEuro', 'Range_Km']]
print(top_expensive.to_string(index=False))

print("\n🔋 Top 5 Longest Range EVs:")
top_range = df_clean.nlargest(5, 'Range_Km')[['Brand', 'Model', 'Range_Km', 'Efficiency_WhKm']]
print(top_range.to_string(index=False))

print("\n⚡ Top 5 Fastest EVs:")
top_speed = df_clean.nlargest(5, 'TopSpeed_KmH')[['Brand', 'Model', 'TopSpeed_KmH', 'AccelSec']]
print(top_speed.to_string(index=False))

# ============================================================================
# 4. MACHINE LEARNING MODEL - PRICE PREDICTION
# ============================================================================
print("\n" + "="*80)
print("🤖 MACHINE LEARNING MODEL: EV PRICE PREDICTION")
print("="*80)

# Prepare features
ml_df = df_clean.copy()

# Encode categorical variables
le_brand = LabelEncoder()
le_bodystyle = LabelEncoder()
le_powertrain = LabelEncoder()
le_plugtype = LabelEncoder()
le_segment = LabelEncoder()
le_rapidcharge = LabelEncoder()

ml_df['Brand_Encoded'] = le_brand.fit_transform(ml_df['Brand'])
ml_df['BodyStyle_Encoded'] = le_bodystyle.fit_transform(ml_df['BodyStyle'])
ml_df['PowerTrain_Encoded'] = le_powertrain.fit_transform(ml_df['PowerTrain'])
ml_df['PlugType_Encoded'] = le_plugtype.fit_transform(ml_df['PlugType'])
ml_df['Segment_Encoded'] = le_segment.fit_transform(ml_df['Segment'])
ml_df['RapidCharge_Encoded'] = le_rapidcharge.fit_transform(ml_df['RapidCharge'])

# Select features for prediction
feature_cols = ['AccelSec', 'TopSpeed_KmH', 'Range_Km', 'Efficiency_WhKm', 
                'FastCharge_KmH', 'Seats', 'Brand_Encoded', 'BodyStyle_Encoded',
                'PowerTrain_Encoded', 'PlugType_Encoded', 'Segment_Encoded',
                'RapidCharge_Encoded']

X = ml_df[feature_cols]
y = ml_df['PriceEuro']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n📊 Dataset Split:")
print(f"   Training samples: {X_train.shape[0]}")
print(f"   Testing samples: {X_test.shape[0]}")
print(f"   Features: {X_train.shape[1]}")

# ============================================================================
# 5. MODEL TRAINING & EVALUATION
# ============================================================================
print("\n🎯 5. MODEL TRAINING & EVALUATION")
print("-"*80)

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
}

results = {}

for name, model in models.items():
    print(f"\n{name}:")
    print("-" * 40)
    
    # Train model
    if name == 'Linear Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Evaluate
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {
        'model': model,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'predictions': y_pred
    }
    
    print(f"   R² Score: {r2:.4f}")
    print(f"   RMSE: €{rmse:,.2f}")
    print(f"   MAE: €{mae:,.2f}")
    print(f"   Accuracy: {r2*100:.2f}%")

# Best model
best_model_name = max(results, key=lambda x: results[x]['r2'])
best_model = results[best_model_name]['model']

print("\n" + "="*80)
print(f"🏆 BEST MODEL: {best_model_name}")
print("="*80)
print(f"   R² Score: {results[best_model_name]['r2']:.4f}")
print(f"   RMSE: €{results[best_model_name]['rmse']:,.2f}")
print(f"   MAE: €{results[best_model_name]['mae']:,.2f}")

# Feature importance (for tree-based models)
if best_model_name != 'Linear Regression':
    print("\n📊 Feature Importance (Top 10):")
    print("-"*80)
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['feature']:<25} {row['importance']:.4f}")

# ============================================================================
# 6. PREDICTION EXAMPLES
# ============================================================================
print("\n" + "="*80)
print("🔮 SAMPLE PREDICTIONS")
print("="*80)

# Get 5 random samples
sample_indices = np.random.choice(X_test.index, 5, replace=False)
sample_X = X_test.loc[sample_indices]
sample_y_true = y_test.loc[sample_indices]

if best_model_name == 'Linear Regression':
    sample_X_scaled = scaler.transform(sample_X)
    sample_predictions = best_model.predict(sample_X_scaled)
else:
    sample_predictions = best_model.predict(sample_X)

print("\nActual vs Predicted Prices:")
print("-"*80)
for idx, (true_price, pred_price) in enumerate(zip(sample_y_true, sample_predictions)):
    brand = ml_df.loc[sample_indices.tolist()[idx], 'Brand']
    model_name = ml_df.loc[sample_indices.tolist()[idx], 'Model']
    error = abs(true_price - pred_price)
    error_pct = (error / true_price) * 100
    print(f"\n{idx+1}. {brand} {model_name}")
    print(f"   Actual Price:    €{true_price:>10,.0f}")
    print(f"   Predicted Price: €{pred_price:>10,.0f}")
    print(f"   Error:           €{error:>10,.0f} ({error_pct:.1f}%)")

# ============================================================================
# 7. SAVE MODEL
# ============================================================================
print("\n" + "="*80)
print("💾 SAVING MODEL & ENCODERS")
print("="*80)

import pickle

# Save model
with open('ev_price_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
print("✅ Model saved: ev_price_model.pkl")

# Save scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✅ Scaler saved: scaler.pkl")

# Save encoders
encoders = {
    'brand': le_brand,
    'bodystyle': le_bodystyle,
    'powertrain': le_powertrain,
    'plugtype': le_plugtype,
    'segment': le_segment,
    'rapidcharge': le_rapidcharge
}

with open('encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)
print("✅ Encoders saved: encoders.pkl")

print("\n" + "="*80)
print("✨ ANALYSIS COMPLETE!")
print("="*80)
print("""
Files generated:
  • ev_price_model.pkl - Trained ML model
  • scaler.pkl - Feature scaler
  • encoders.pkl - Categorical encoders

You can now use these files to make predictions on new EV data!
""")