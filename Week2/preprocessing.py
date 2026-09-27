"""
Week 2 - Logistics Data Collection, Cleaning and Preprocessing

This script:
1. Loads the raw logistics CSV.
2. Profiles data quality.
3. Cleans duplicates, missing values, categories and invalid values.
4. Validates dates and business rules.
5. Detects IQR outliers without blindly deleting legitimate observations.
6. Creates derived logistics variables.
7. Creates a standardized dataset for scale-sensitive analysis.
8. Exports cleaned data and a data-quality report.

Run:
    python preprocessing.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "logistics_raw.csv"
CLEAN_FILE = BASE_DIR / "logistics_cleaned.csv"
SCALED_FILE = BASE_DIR / "logistics_scaled.csv"
REPORT_FILE = BASE_DIR / "data_quality_report.csv"


def iqr_bounds(series: pd.Series):
    """Return lower and upper IQR screening bounds."""
    clean = series.dropna()
    q1 = clean.quantile(0.25)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def profile_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Create a compact data-quality profile."""
    rows = []
    for col in df.columns:
        rows.append({
            "check": "missing_values",
            "field": col,
            "count": int(df[col].isna().sum()),
            "detail": f"{df[col].isna().mean()*100:.2f}% missing"
        })
    rows.append({
        "check": "duplicate_rows",
        "field": "__all__",
        "count": int(df.duplicated().sum()),
        "detail": "Exact duplicate rows"
    })
    return pd.DataFrame(rows)


def main():
    # 1. Load
    df = pd.read_csv(RAW_FILE)
    original_rows = len(df)

    # 2. Standardize names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )

    # 3. Convert data types
    for col in ["order_date", "shipping_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    numeric_cols = [
        "distance_km", "order_weight_kg", "order_value",
        "fuel_used_l", "delivery_days_actual",
        "delivery_days_scheduled", "vehicle_capacity_kg"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Quality counts before cleaning
    missing_before = int(df.isna().sum().sum())
    duplicate_before = int(df.duplicated().sum())
    negative_distance_before = int((df["distance_km"] < 0).sum())
    negative_fuel_before = int((df["fuel_used_l"] < 0).sum())
    invalid_dates_before = int(
        (df["shipping_date"] < df["order_date"]).fillna(False).sum()
    )

    # 4. Remove exact duplicates
    df = df.drop_duplicates().copy()

    # 5. Standardize categorical fields
    for col in ["shipping_mode", "traffic_level", "customer_segment"]:
        df[col] = df[col].astype("string").str.strip()

    shipping_map = {
        "std": "standard",
        "standard": "standard",
        "first class": "first_class",
        "second class": "second_class",
        "same day": "same_day"
    }
    df["shipping_mode"] = (
        df["shipping_mode"].str.lower().replace(shipping_map)
    )

    # 6. Domain validation: impossible values -> missing
    df.loc[df["distance_km"] < 0, "distance_km"] = np.nan
    df.loc[df["order_weight_kg"] <= 0, "order_weight_kg"] = np.nan
    df.loc[df["fuel_used_l"] < 0, "fuel_used_l"] = np.nan
    df.loc[df["vehicle_capacity_kg"] <= 0, "vehicle_capacity_kg"] = np.nan

    # 7. Missing-value handling
    for col in ["distance_km", "order_weight_kg", "fuel_used_l"]:
        df[col] = df[col].fillna(df[col].median())

    for col in ["shipping_mode", "traffic_level", "customer_segment"]:
        df[col] = df[col].fillna("unknown")

    # 8. Date validation
    bad_dates = (
        df["shipping_date"].notna() &
        df["order_date"].notna() &
        (df["shipping_date"] < df["order_date"])
    )
    invalid_dates_after_flagging = int(bad_dates.sum())
    df.loc[bad_dates, "shipping_date"] = pd.NaT

    # 9. Derived variables
    df["actual_lead_days"] = (
        df["shipping_date"] - df["order_date"]
    ).dt.days

    df["shipping_delay_days"] = (
        df["delivery_days_actual"] -
        df["delivery_days_scheduled"]
    )

    # 10. IQR outlier screening
    low, high = iqr_bounds(df["order_value"])
    iqr_outlier_mask = (
        (df["order_value"] < low) |
        (df["order_value"] > high)
    )
    iqr_outlier_count = int(iqr_outlier_mask.sum())

    # Important: outliers are flagged, not automatically deleted.
    df["order_value_iqr_outlier"] = iqr_outlier_mask.astype(int)

    # 11. Final validation
    final_missing = int(df.isna().sum().sum())
    final_duplicates = int(df.duplicated().sum())
    final_negative_distance = int((df["distance_km"] < 0).sum())
    final_negative_fuel = int((df["fuel_used_l"] < 0).sum())

    # 12. Save clean dataset
    df.to_csv(CLEAN_FILE, index=False)

    # 13. Create scaled copy for clustering/distance-based analysis
    scale_cols = [
        "distance_km",
        "order_weight_kg",
        "order_value",
        "delivery_days_actual"
    ]
    scaled = df.copy()
    scaler = StandardScaler()
    scaled[scale_cols] = scaler.fit_transform(scaled[scale_cols])
    scaled.to_csv(SCALED_FILE, index=False)

    # 14. Quality report
    report = pd.DataFrame([
        ["rows_loaded", original_rows, "Raw row count"],
        ["exact_duplicates_before", duplicate_before, "Exact duplicate rows removed"],
        ["missing_values_before", missing_before, "Total missing cells before cleaning"],
        ["negative_distance_before", negative_distance_before, "Physically invalid distance values"],
        ["negative_fuel_before", negative_fuel_before, "Physically invalid fuel values"],
        ["invalid_dates_before", invalid_dates_before, "Shipping date earlier than order date"],
        ["invalid_dates_flagged_after_cleaning", invalid_dates_after_flagging, "Set to missing for source review"],
        ["iqr_order_value_outliers", iqr_outlier_count, "Flagged, not blindly deleted"],
        ["rows_after_cleaning", len(df), "Rows after duplicate removal"],
        ["missing_values_after", final_missing, "Remaining missing cells"],
        ["duplicates_after", final_duplicates, "Remaining exact duplicates"],
        ["negative_distance_after", final_negative_distance, "Remaining invalid distances"],
        ["negative_fuel_after", final_negative_fuel, "Remaining invalid fuel values"],
    ], columns=["metric", "count", "description"])

    report.to_csv(REPORT_FILE, index=False)

    print("=" * 60)
    print("LOGISTICS PREPROCESSING COMPLETE")
    print("=" * 60)
    print(f"Raw file:       {RAW_FILE.name}")
    print(f"Clean file:     {CLEAN_FILE.name}")
    print(f"Scaled file:    {SCALED_FILE.name}")
    print(f"Quality report: {REPORT_FILE.name}")
    print()
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
