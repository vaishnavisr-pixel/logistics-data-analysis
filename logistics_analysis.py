import pandas as pd
import matplotlib.pyplot as plt

# Week 1 logistics analysis starter script.
# Expected input columns:
# Order_ID, Order_Date, Warehouse, Product_ID, Quantity, Destination,
# Distance_km, Planned_Delivery_Date, Actual_Delivery_Date,
# Transport_Mode, Transport_Cost, Inventory_Level

df = pd.read_csv("logistics_data.csv")

# Convert date fields
for col in ["Order_Date", "Planned_Delivery_Date", "Actual_Delivery_Date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Basic data-quality checks
print(df.info())
print("\nMissing values:\n", df.isna().sum())

# Derived metrics
df["Delivery_Days"] = (df["Actual_Delivery_Date"] - df["Order_Date"]).dt.days
df["On_Time"] = df["Actual_Delivery_Date"] <= df["Planned_Delivery_Date"]

# KPIs
on_time_rate = df["On_Time"].mean() * 100
average_delivery_days = df["Delivery_Days"].mean()
average_transport_cost = df["Transport_Cost"].mean()

print(f"On-time delivery rate: {on_time_rate:.2f}%")
print(f"Average delivery time: {average_delivery_days:.2f} days")
print(f"Average transport cost/order: {average_transport_cost:.2f}")

# Example chart
df.groupby("Transport_Mode")["Transport_Cost"].mean().plot(kind="bar")
plt.title("Average Transportation Cost by Mode")
plt.xlabel("Transport Mode")
plt.ylabel("Average Cost")
plt.tight_layout()
plt.show()
