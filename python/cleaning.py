# ============================================================
# PROJECT  : Hospital Emergency Room Analytics
# FILE     : cleaning.py
# PURPOSE  : Load, inspect, clean and export ER dataset
# ANALYST  : Ovean S
# DATE     : October 2026
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# FILE PATHS
# ============================================================
RAW_DATA_PATH     = 'E:/projects/HealthCare/data/hospital_er_raw.csv'
CLEAN_DATA_PATH   = 'E:/projects/HealthCare/data/hospital_er_clean.csv'
CHARTS_PATH       = 'E:/projects/HealthCare/insights/'

# ============================================================
# STEP 1 : LOAD DATA
# ============================================================
def load_data(path):
    """
    Load CSV file into a pandas DataFrame.
    
    Args:
        path (str): File path to the CSV file
    
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    print("=" * 55)
    print("STEP 1: LOADING DATA")
    print("=" * 55)
    
    df = pd.read_csv(path)
    print(f"✅ Data loaded successfully")
    print(f"   Rows    : {df.shape[0]}")
    print(f"   Columns : {df.shape[1]}")
    return df

# ============================================================
# STEP 2 : INSPECT DATA
# ============================================================
def inspect_data(df):
    """
    Print full inspection report of the dataframe.
    
    Args:
        df (pd.DataFrame): Raw dataframe to inspect
    """
    print("\n" + "=" * 55)
    print("STEP 2: DATA INSPECTION REPORT")
    print("=" * 55)
    
    print("\n📋 COLUMN DATA TYPES:")
    print(df.dtypes)
    
    print("\n❓ MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    missing_report = pd.DataFrame({
        'Missing Count' : missing,
        'Missing %'     : missing_pct
    })
    print(missing_report[missing_report['Missing Count'] > 0])
    
    print("\n📊 BASIC STATISTICS:")
    print(df[['patient_age', 'patient_wait_time', 
              'satisfaction_score']].describe().round(2))
    
    print("\n🔢 DUPLICATE ROWS:", df.duplicated().sum())

# ============================================================
# STEP 3 : CLEAN DATA
# ============================================================
def clean_data(df):
    """
    Clean the raw dataframe:
    - Fix data types
    - Handle missing values
    - Remove duplicates
    - Standardize text columns
    
    Args:
        df (pd.DataFrame): Raw dataframe
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print("\n" + "=" * 55)
    print("STEP 3: CLEANING DATA")
    print("=" * 55)
    
    # Fix date column
    df['admission_date'] = pd.to_datetime(df['admission_date'])
    print("✅ admission_date converted to datetime")
    
    # Handle missing satisfaction scores
    # Fill with median — better than mean because
    # satisfaction scores can be skewed by outliers
    median_score = df['satisfaction_score'].median()
    df['satisfaction_score'] = df['satisfaction_score'].fillna(median_score)
    print(f"✅ Missing satisfaction scores filled with median: {median_score}")
    
    # Standardize text columns — remove extra spaces, fix casing
    text_columns = ['patient_gender', 'patient_race', 
                    'department_referral', 'age_group']
    for col in text_columns:
        df[col] = df[col].str.strip().str.title()
    print("✅ Text columns standardized")
    
    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"✅ Duplicates removed: {before - after} rows dropped")
    
    # Fix boolean column
    df['admission_flag'] = df['admission_flag'].astype(str).str.strip()
    
    print(f"\n✅ Cleaning complete — {len(df)} rows remaining")
    return df

# ============================================================
# MAIN — runs all steps in order
# ============================================================
if __name__ == "__main__":
    
    # Step 1: Load
    df_raw = load_data(RAW_DATA_PATH)
    
    # Step 2: Inspect
    inspect_data(df_raw)
    
    # Step 3: Clean
    df_clean = clean_data(df_raw)
    
    # Step 4: Save clean file
    df_clean.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"\n💾 Clean data saved to: {CLEAN_DATA_PATH}")
    
    print("\n" + "=" * 55)
    print("✅ CLEANING PIPELINE COMPLETE")
    print("=" * 55)