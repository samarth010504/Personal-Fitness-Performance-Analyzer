# analysis.py

import pandas as pd
import numpy as np


# ============================================
# 1️⃣ LOAD DATA
# ============================================

df = pd.read_csv("data/fitness_data.csv")

df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)


# ============================================
# 2️⃣ DATA VALIDATION
# ============================================

print("\n===== DATA INFO =====")
print(df.info())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


# ============================================
# 3️⃣ FEATURE ENGINEERING
# ============================================

# Speed (if not already present)
df["Speed_kmph"] = df["Distance_km"] / (df["Time_min"] / 60)

# Pace (minutes per km)
df["Pace_min_per_km"] = df["Time_min"] / df["Distance_km"]

# 7-day rolling averages
df["Rolling_7D_Speed"] = df["Speed_kmph"].rolling(window=7).mean()
df["Rolling_7D_Weight"] = df["Weight_kg"].rolling(window=7).mean()

# Weekly total distance
weekly_distance = df["Distance_km"].resample("W").sum()

# Cumulative distance
df["Cumulative_Distance"] = df["Distance_km"].cumsum()


# ============================================
# 4️⃣ STATISTICAL ANALYSIS (NumPy Focus)
# ============================================

speed_array = df["Speed_kmph"].values
weight_array = df["Weight_kg"].values

print("\n===== STATISTICS =====")

print("Average Speed:", np.mean(speed_array))
print("Speed Std Dev:", np.std(speed_array))
print("Speed Variance:", np.var(speed_array))
print("Max Speed:", np.max(speed_array))
print("Min Speed:", np.min(speed_array))

print("\nAverage Weight:", np.mean(weight_array))
print("Weight Std Dev:", np.std(weight_array))


# ============================================
# 5️⃣ CORRELATION ANALYSIS
# ============================================

correlation_matrix = np.corrcoef(
    df["Weight_kg"],
    df["Speed_kmph"]
)

print("\n===== CORRELATION =====")
print("Correlation (Weight vs Speed):", correlation_matrix[0, 1])


# ============================================
# 6️⃣ WEEKLY & MONTHLY ANALYSIS
# ============================================

weekly_avg_speed = df["Speed_kmph"].resample("W").mean()
monthly_avg_speed = df["Speed_kmph"].resample("M").mean()

print("\n===== WEEKLY AVG SPEED =====")
print(weekly_avg_speed)

print("\n===== MONTHLY AVG SPEED =====")
print(monthly_avg_speed)


# ============================================
# 7️⃣ PERFORMANCE SUMMARY
# ============================================

overall_improvement = (
    df["Speed_kmph"].iloc[-1] - df["Speed_kmph"].iloc[0]
)

print("\n===== PERFORMANCE SUMMARY =====")
print(f"Total Speed Improvement: {overall_improvement:.2f} km/h")

print("Total Distance Covered:",
      df["Distance_km"].sum(), "km")