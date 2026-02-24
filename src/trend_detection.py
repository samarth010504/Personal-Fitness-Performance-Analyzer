# trend_detection.py

import pandas as pd
import numpy as np


# ============================================
# 1️⃣ LOAD & PREPARE DATA
# ============================================

df = pd.read_csv("data/fitness_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)

# Ensure speed exists
df["Speed_kmph"] = df["Distance_km"] / (df["Time_min"] / 60)

# Rolling average speed
df["Rolling_7D_Speed"] = df["Speed_kmph"].rolling(window=7).mean()


# ============================================
# 2️⃣ IMPROVEMENT DETECTION
# ============================================

# Compare current 7-day avg with previous 7-day avg
df["Speed_Trend"] = df["Rolling_7D_Speed"].diff()

improvement_threshold = 0.05  # km/h improvement

df["Improving"] = df["Speed_Trend"] > improvement_threshold


# ============================================
# 3️⃣ PLATEAU DETECTION
# ============================================

plateau_threshold = 0.02  # minimal speed change
plateau_window = 10       # number of days

# Calculate absolute speed change
df["Abs_Speed_Change"] = df["Speed_kmph"].diff().abs()

# Rolling average of speed change
df["Rolling_Speed_Change"] = df["Abs_Speed_Change"].rolling(window=plateau_window).mean()

df["Plateau"] = df["Rolling_Speed_Change"] < plateau_threshold


# ============================================
# 4️⃣ SUMMARY INSIGHTS
# ============================================

total_improvement = df["Speed_kmph"].iloc[-1] - df["Speed_kmph"].iloc[0]

correlation = np.corrcoef(df["Weight_kg"], df["Speed_kmph"])[0, 1]

plateau_days = df[df["Plateau"] == True].index

print("\n===== TREND DETECTION SUMMARY =====")

print(f"Total Speed Improvement: {total_improvement:.2f} km/h")

print(f"Weight vs Speed Correlation: {correlation:.2f}")

if len(plateau_days) > 0:
    print("Plateau detected on:")
    print(plateau_days)
else:
    print("No significant plateau detected.")

improving_days = df[df["Improving"] == True].index

print(f"Number of improving days: {len(improving_days)}")