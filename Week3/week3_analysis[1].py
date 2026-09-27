"""
Week 3 - Advanced Data Analysis and Visualization in Logistics
Reproducible EDA script.

Input:
    week3_logistics_analysis_data.csv

Outputs:
    summary_statistics.csv
    correlation_matrix.csv
    traffic_kpi_summary.csv
    charts/*.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "week3_logistics_analysis_data.csv")

numeric = [
    "Distance_km", "Order_Weight_kg", "Delivery_Days_Actual",
    "Fuel_Used_L", "Transportation_Cost", "Delay_Days"
]

# Descriptive statistics
summary = df[numeric].describe().T
summary["missing"] = df[numeric].isna().sum()
summary["median"] = df[numeric].median()
summary.to_csv(BASE / "summary_statistics.csv")

# Correlations
corr = df[numeric].corr()
corr.to_csv(BASE / "correlation_matrix.csv")

# KPI comparison by traffic
kpi = df.groupby("Traffic_Level").agg(
    Orders=("Order_ID","count"),
    Avg_Delivery_Days=("Delivery_Days_Actual","mean"),
    Avg_Delay_Days=("Delay_Days","mean"),
    Late_Rate=("Delivery_Status", lambda x: (x=="Late").mean()*100),
    Avg_Transport_Cost=("Transportation_Cost","mean")
).reset_index()
kpi.to_csv(BASE / "traffic_kpi_summary.csv", index=False)

chart_dir = BASE / "charts"
chart_dir.mkdir(exist_ok=True)

# 1. Distribution
plt.figure(figsize=(8,5))
plt.hist(df["Delivery_Days_Actual"], bins=range(1, df["Delivery_Days_Actual"].max()+2), edgecolor="black")
plt.title("Distribution of Actual Delivery Days")
plt.xlabel("Actual delivery days")
plt.ylabel("Number of orders")
plt.tight_layout()
plt.savefig(chart_dir/"01_delivery_distribution.png", dpi=180)
plt.close()

# 2. Distance and cost relationship
plt.figure(figsize=(8,5))
plt.scatter(df["Distance_km"], df["Transportation_Cost"], alpha=.35)
plt.title("Distance vs Transportation Cost")
plt.xlabel("Distance (km)")
plt.ylabel("Transportation cost")
plt.tight_layout()
plt.savefig(chart_dir/"02_distance_vs_cost.png", dpi=180)
plt.close()

# 3. Traffic and delivery time
order = ["Low","Medium","High"]
means = df.groupby("Traffic_Level")["Delivery_Days_Actual"].mean().reindex(order)
plt.figure(figsize=(7,5))
plt.bar(means.index, means.values)
plt.title("Average Delivery Time by Traffic Level")
plt.xlabel("Traffic level")
plt.ylabel("Average actual delivery days")
plt.tight_layout()
plt.savefig(chart_dir/"03_traffic_delivery.png", dpi=180)
plt.close()

# 4. Delay distribution
plt.figure(figsize=(8,5))
plt.boxplot([df.loc[df["Traffic_Level"]==t,"Delay_Days"] for t in order], labels=order)
plt.title("Delivery Delay Distribution by Traffic Level")
plt.xlabel("Traffic level")
plt.ylabel("Delay days")
plt.tight_layout()
plt.savefig(chart_dir/"04_delay_by_traffic.png", dpi=180)
plt.close()

# 5. Correlation matrix
plt.figure(figsize=(8,5))
plt.imshow(corr.values, aspect="auto")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
plt.yticks(range(len(corr.index)), corr.index)
plt.title("Correlation Matrix of Key Numeric Variables")
plt.colorbar(label="Correlation")
plt.tight_layout()
plt.savefig(chart_dir/"05_correlation_matrix.png", dpi=180)
plt.close()

print("Week 3 analysis completed successfully.")
