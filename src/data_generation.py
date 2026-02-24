import numpy as np
import pandas as pd
from pathlib import Path

# Set seed for reproducibility
np.random.seed(42)

days = 60

# Generate dates
dates = pd.date_range(start="2026-01-01", periods=days)

# Distance: 2km to 5km gradually increasing
distance = np.linspace(2, 5, days) + np.random.normal(0, 0.2, days)

# Pace improving (minutes per km)
pace = np.linspace(6.5, 5.2, days) + np.random.normal(0, 0.1, days)

# Time = distance * pace
time = distance * pace

# Calories (roughly proportional to distance)
calories = distance * 60 + np.random.normal(0, 10, days)

# Weight decreasing gradually
weight = np.linspace(70, 67, days) + np.random.normal(0, 0.3, days)

# Create DataFrame
df = pd.DataFrame({
    "Date": dates,
    "Distance_km": distance,
    "Time_min": time,
    "Calories": calories,
    "Weight_kg": weight
})

# Calculate Speed
df["Speed_kmph"] = df["Distance_km"] / (df["Time_min"] / 60)
# Ensure output directory exists and write CSV relative to project root
base = Path(__file__).resolve().parents[1]
out = base / "data" / "fitness_data.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False, date_format="%Y-%m-%d", float_format="%.2f")

print(f"Wrote {out}")
print(df.head().to_string(index=False))
