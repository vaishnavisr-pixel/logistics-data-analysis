# Week 2 – Logistics Data Collection, Cleaning and Preprocessing

## Project Overview

This repository contains the practical implementation for **Week 2: Data Collection, Cleaning, and Preprocessing for Logistics Analysis**.

The project prepares logistics data for the Week 1 analytics roadmap, which includes delivery-time prediction, clustering, KPI analysis, and route/vehicle optimization.

The workflow demonstrates:

- Data collection simulation
- Data profiling
- Duplicate detection and removal
- Missing-value handling
- Categorical standardization
- Invalid-value detection
- Date validation
- Outlier detection using domain rules and the IQR method
- Derived logistics variables
- Standardization for scale-sensitive analysis
- Final data-quality validation
- Reproducible CSV export

## Reference Dataset

The report uses the **DataCo Smart Supply Chain for Big Data Analysis** dataset as the public reference dataset/schema.

Public reference:
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

The CSV included in this repository is a **simulated demonstration dataset** based on the logistics/supply-chain structure. It intentionally contains controlled quality problems so the preprocessing pipeline can be demonstrated reproducibly.

The sample must not be presented as a copy of the original public records.

## Repository Structure

```text
Week2/
│
├── preprocessing.py
├── logistics_raw.csv
├── logistics_cleaned.csv
├── logistics_scaled.csv
├── data_quality_report.csv
└── README.md
```

## Dataset Fields

| Field | Meaning |
|---|---|
| Order_ID | Unique order identifier |
| Order_Date | Date order was placed |
| Shipping_Date | Date shipment was dispatched |
| Shipping_Mode | Shipping service level |
| Delivery_Days_Actual | Actual delivery duration |
| Delivery_Days_Scheduled | Scheduled delivery duration |
| Distance_km | Estimated delivery distance |
| Order_Weight_kg | Shipment weight |
| Order_Value | Order monetary value |
| Fuel_Used_L | Estimated fuel consumed |
| Traffic_Level | Traffic condition |
| Vehicle_Capacity_kg | Vehicle capacity |
| Customer_Segment | Customer category |
| Delivery_Status | On-time/late status |
| Late_Delivery_Risk | Binary delivery-risk indicator |

## Data Quality Problems Simulated

The raw sample contains controlled examples of:

- Missing distance values
- Missing shipment weights
- Missing traffic levels
- Exact duplicate rows
- Negative distance values
- Negative fuel values
- Extreme order values
- Invalid shipping/order date sequences
- Inconsistent shipping-mode labels

This makes the repository demonstrate actual preprocessing rather than only providing pseudocode.

## Cleaning Methodology

### 1. Column and data-type standardization

Column names are converted to lowercase snake_case. Date fields are converted to datetime and numerical fields are converted to numeric types.

### 2. Duplicate removal

Exact duplicate rows are removed after confirming that the simulated data is transaction-level.

### 3. Missing numerical values

Missing distance, weight and fuel values are imputed using the median after invalid values are converted to missing.

Median is used because logistics variables can be skewed by long-distance or high-value orders.

### 4. Missing categorical values

Missing categorical values are assigned an explicit `unknown` category rather than being silently assigned the most common class.

### 5. Category standardization

Variants such as:

- `STD`
- `Standard`
- `standard `

are mapped to the canonical `standard` category.

### 6. Domain validation

Physically impossible values such as negative distance and negative fuel consumption are treated as invalid.

### 7. Date validation

Shipping dates earlier than order dates are flagged as invalid and set to missing for source-system review.

### 8. Outlier detection

The IQR method is used to flag unusually high or low order values.

Outliers are **not automatically deleted** because a high-value order can be a legitimate business event.

### 9. Derived variables

The pipeline creates:

- `actual_lead_days`
- `shipping_delay_days`
- `order_value_iqr_outlier`

### 10. Standardization

A scaled copy of the dataset is generated using `StandardScaler`.

This is useful for algorithms such as K-Means where feature scale affects distance calculations.

## How to Run

Install the dependencies:

```bash
pip install pandas numpy scikit-learn
```

Then run:

```bash
python preprocessing.py
```

The script generates:

```text
logistics_cleaned.csv
logistics_scaled.csv
data_quality_report.csv
```

## Validation

The script checks that:

- Duplicate rows are removed
- Distances are non-negative
- Fuel consumption is non-negative
- Date sequences are logically valid
- Numeric variables are usable
- Categorical variables are standardized
- The final quality report documents the transformation

## Why This Matters for Logistics

Data quality affects every later stage of the project.

For example:

- Duplicate deliveries can inflate on-time delivery KPIs.
- Missing distance can distort transportation-cost analysis.
- Invalid dates can corrupt delivery-time calculations.
- Extreme values can influence regression models.
- Unscaled features can distort clustering.
- Invalid vehicle capacity values can produce infeasible allocation decisions.

Therefore, preprocessing is treated as a business-validation step rather than only a technical cleaning exercise.

## Connection to Week 1

The cleaned dataset is designed to support the Week 1 roadmap:

```text
Raw Logistics Data
        ↓
Data Cleaning & Validation
        ↓
Exploratory Data Analysis
        ↓
Regression / Delivery Prediction
        ↓
Customer & Route Clustering
        ↓
Vehicle / Route Optimization
        ↓
KPI Evaluation
```

## Important Note

The numerical results in this repository are from the **simulated demonstration sample**. They should not be reported as measured results from the original DataCo dataset.

For a production project, the same pipeline should be connected to the actual downloaded dataset or an organization's operational database.

## Author

Week 2 Logistics Data Analysis Project
