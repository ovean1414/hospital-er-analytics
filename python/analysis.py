# ============================================================
# PROJECT  : Hospital Emergency Room Analytics
# FILE     : analysis.py
# PURPOSE  : Analyze cleaned ER data to answer business
#            questions and generate charts
# ANALYST  : Ovean S
# DATE     : October 2026
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Chart style — professional look
sns.set_theme(style="darkgrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'sans-serif'

# ============================================================
# PATHS
# ============================================================
CLEAN_DATA_PATH = 'E:/projects/HealthCare/data/hospital_er_clean.csv'
CHARTS_PATH     = 'E:/projects/HealthCare/insights/'

# Create insights folder if it doesn't exist
os.makedirs(CHARTS_PATH, exist_ok=True)

# ============================================================
# LOAD CLEAN DATA
# ============================================================
def load_clean_data(path):
    """Load the cleaned dataset for analysis."""
    df = pd.read_csv(path)
    df['admission_date'] = pd.to_datetime(df['admission_date'])
    print(f"✅ Clean data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# ============================================================
# ANALYSIS 1 : EXECUTIVE SUMMARY METRICS
# ============================================================
def executive_summary(df):
    """Calculate and print top-level business KPIs."""
    print("\n" + "=" * 55)
    print("ANALYSIS 1: EXECUTIVE SUMMARY")
    print("=" * 55)

    total_patients      = len(df)
    avg_wait_time       = df['patient_wait_time'].mean().round(2)
    avg_satisfaction    = df['satisfaction_score'].mean().round(2)
    admission_rate = df['admission_flag'].astype(str).str.strip().str.capitalize().value_counts(normalize=True).get('True', 0) * 100
    busiest_dept        = df[df['department_referral'] != 'None']['department_referral'].value_counts().index[0]
    pct_long_wait       = (df['patient_wait_time'] > 45).sum() / total_patients * 100

    print(f"\n  📊 Total Patients        : {total_patients:,}")
    print(f"  ⏱️  Avg Wait Time         : {avg_wait_time} mins")
    print(f"  ⭐ Avg Satisfaction      : {avg_satisfaction} / 10")
    print(f"  🏥 Admission Rate        : {admission_rate:.1f}%")
    print(f"  🔝 Busiest Department    : {busiest_dept}")
    print(f"  ⚠️  Patients Waiting >45m : {pct_long_wait:.1f}%")

    return {
        'total_patients'   : total_patients,
        'avg_wait_time'    : avg_wait_time,
        'avg_satisfaction' : avg_satisfaction,
        'admission_rate'   : round(admission_rate, 1),
        'busiest_dept'     : busiest_dept,
        'pct_long_wait'    : round(pct_long_wait, 1)
    }

# ============================================================
# ANALYSIS 2 : PEAK HOURS ANALYSIS
# ============================================================
def peak_hours_analysis(df):
    """Identify busiest hours and their impact on wait time."""
    print("\n" + "=" * 55)
    print("ANALYSIS 2: PEAK HOURS ANALYSIS")
    print("=" * 55)

    hourly = df.groupby('hour').agg(
        Patient_Count  = ('patient_id', 'count'),
        Avg_Wait_Time  = ('patient_wait_time', 'mean'),
        Avg_Satisfaction = ('satisfaction_score', 'mean')
    ).round(2)

    print(hourly)

    # Chart
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].bar(hourly.index, hourly['Patient_Count'],
                color='steelblue', edgecolor='white')
    axes[0].set_title('Patient Volume by Hour of Day', 
                       fontsize=14, fontweight='bold', pad=15)
    axes[0].set_xlabel('Hour of Day (0 = Midnight, 12 = Noon)')
    axes[0].set_ylabel('Number of Patients')
    axes[0].set_xticks(range(0, 24))

    axes[1].plot(hourly.index, hourly['Avg_Wait_Time'],
                 color='coral', marker='o', linewidth=2)
    axes[1].set_title('Average Wait Time by Hour of Day',
                       fontsize=14, fontweight='bold', pad=15)
    axes[1].set_xlabel('Hour of Day')
    axes[1].set_ylabel('Avg Wait Time (mins)')
    axes[1].set_xticks(range(0, 24))
    axes[1].axhline(y=45, color='red', linestyle='--',
                    label='45-min threshold')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(f'{CHARTS_PATH}peak_hours_analysis.png')
    plt.close()
    print(f"\n✅ Chart saved: peak_hours_analysis.png")

# ============================================================
# ANALYSIS 3 : DEPARTMENT PERFORMANCE
# ============================================================
def department_analysis(df):
    """Analyze performance metrics by department."""
    print("\n" + "=" * 55)
    print("ANALYSIS 3: DEPARTMENT PERFORMANCE")
    print("=" * 55)

    dept = df[df['department_referral'] != 'None'].groupby(
        'department_referral').agg(
        Patient_Count    = ('patient_id', 'count'),
        Avg_Wait_Time    = ('patient_wait_time', 'mean'),
        Avg_Satisfaction = ('satisfaction_score', 'mean')
    ).round(2).sort_values('Avg_Wait_Time', ascending=False)

    print(dept)

    # Chart
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    colors = sns.color_palette('Blues_r', len(dept))

    axes[0].barh(dept.index, dept['Avg_Wait_Time'], color=colors)
    axes[0].set_title('Avg Wait Time by Department',
                       fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Avg Wait Time (mins)')
    axes[0].axvline(x=45, color='red', linestyle='--',
                    label='45-min threshold')
    axes[0].legend()

    axes[1].barh(dept.index, dept['Avg_Satisfaction'],
                 color=sns.color_palette('Greens_r', len(dept)))
    axes[1].set_title('Avg Satisfaction by Department',
                       fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Avg Satisfaction Score (out of 10)')

    plt.tight_layout()
    plt.savefig(f'{CHARTS_PATH}department_analysis.png')
    plt.close()
    print(f"\n✅ Chart saved: department_analysis.png")

# ============================================================
# ANALYSIS 4 : PATIENT DEMOGRAPHICS & SATISFACTION
# ============================================================
def demographics_analysis(df):
    """Analyze satisfaction and wait time by age group and day."""
    print("\n" + "=" * 55)
    print("ANALYSIS 4: DEMOGRAPHICS ANALYSIS")
    print("=" * 55)

    # Age group analysis
    age_analysis = df.groupby('age_group').agg(
        Patient_Count    = ('patient_id', 'count'),
        Avg_Wait_Time    = ('patient_wait_time', 'mean'),
        Avg_Satisfaction = ('satisfaction_score', 'mean')
    ).round(2)

    print("\nBy Age Group:")
    print(age_analysis)

    # Day of week analysis
    day_order = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']
    day_analysis = df.groupby('day_of_week').agg(
        Patient_Count    = ('patient_id', 'count'),
        Avg_Wait_Time    = ('patient_wait_time', 'mean'),
        Avg_Satisfaction = ('satisfaction_score', 'mean')
    ).round(2).reindex(day_order)

    print("\nBy Day of Week:")
    print(day_analysis)

    # Chart
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    age_order = ['0-17', '18-34', '35-49', '50-64', '65+']
    age_plot = age_analysis.reindex(age_order)

    axes[0].bar(age_plot.index,
                age_plot['Avg_Satisfaction'],
                color=sns.color_palette('RdYlGn', len(age_plot)))
    axes[0].set_title('Avg Satisfaction by Age Group',
                       fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Age Group')
    axes[0].set_ylabel('Avg Satisfaction Score')
    axes[0].set_ylim(0, 10)

    axes[1].plot(day_order,
                 day_analysis['Patient_Count'],
                 marker='o', color='steelblue', linewidth=2)
    axes[1].set_title('Patient Volume by Day of Week',
                       fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Day of Week')
    axes[1].set_ylabel('Number of Patients')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_PATH}demographics_analysis.png')
    plt.close()
    print(f"\n✅ Chart saved: demographics_analysis.png")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":

    # Load clean data
    df = load_clean_data(CLEAN_DATA_PATH)

    # Run all analyses
    metrics = executive_summary(df)
    peak_hours_analysis(df)
    department_analysis(df)
    demographics_analysis(df)

    print("\n" + "=" * 55)
    print("✅ ANALYSIS COMPLETE")
    print(f"   Charts saved to: {CHARTS_PATH}")
    print("=" * 55)

print(df['admission_flag'].value_counts())
print(df['admission_flag'].dtype)