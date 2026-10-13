# ============================================================
# PROJECT  : Hospital Emergency Room Analytics
# FILE     : load_to_mysql.py
# PURPOSE  : Load cleaned ER data into MySQL database
# ANALYST  : Ovean S
# DATE     : October 2026
# ============================================================

import pandas as pd
from sqlalchemy import create_engine, text

# ============================================================
# CONFIG — update your MySQL password here
# ============================================================
DB_USER     = 'root'
DB_PASSWORD = 'ovean1414'
DB_HOST     = 'localhost'
DB_NAME     = 'hospital_er'

# ============================================================
# LOAD CSV
# ============================================================
print("Loading clean data...")
df = pd.read_csv('E:/projects/HealthCare/data/hospital_er_clean.csv')

# Fix column names — lowercase, no spaces
df.columns = df.columns.str.lower().str.replace(' ', '_')
print(f"✅ CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"   Columns: {df.columns.tolist()}")

# ============================================================
# CREATE DATABASE IF NOT EXISTS
# ============================================================
print("\nConnecting to MySQL...")

# Connect without specifying database first
engine_root = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}"
)

with engine_root.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    print(f"✅ Database '{DB_NAME}' ready")

# ============================================================
# CONNECT TO DATABASE & LOAD DATA
# ============================================================
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

df.to_sql(
    name       = 'er_visits',
    con        = engine,
    if_exists  = 'replace',
    index      = False
)

print(f"✅ Data loaded into MySQL table: 'er_visits'")
print(f"   Rows loaded: {df.shape[0]}")

# ============================================================
# VERIFY
# ============================================================
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM er_visits"))
    count = result.fetchone()[0]
    print(f"✅ Verified row count in MySQL: {count}")

print("\n✅ DATABASE LOAD COMPLETE")