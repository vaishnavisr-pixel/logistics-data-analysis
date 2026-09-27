# Week 4 – Predictive Modeling and Optimization in Logistics Systems

This project extends Weeks 1–3 into predictive and prescriptive analysis.

## Prediction problem
Target: `Delivery_Days_Actual`

Features: distance, shipment weight, scheduled delivery days, fuel use, traffic level and shipping mode.

Two models are compared:
- Linear Regression — interpretable baseline
- Random Forest Regression — nonlinear ensemble model

Evaluation uses MAE, RMSE and R² on a held-out test set. Five-fold cross-validation and hyperparameter tuning are also performed.

## Optimization
For selected orders, candidate shipping modes are evaluated using predicted delivery time and simulated cost factors. The least-cost mode predicted to meet the scheduled SLA is selected. If no mode meets the SLA, the fastest predicted option is flagged.

This is a transparent scenario optimizer, not a full vehicle-routing solver.

## Files
```text
Week4/
├── README.md
├── week4_predictive_optimization.py
├── week3_logistics_analysis_data.csv
├── model_comparison.csv
├── cross_validation_results.csv
├── tuned_model_results.csv
├── feature_importance.csv
├── optimization_recommendations.csv
└── charts/
    ├── 01_model_mae_comparison.png
    ├── 02_model_rmse_comparison.png
    ├── 03_feature_importance.png
    ├── 04_actual_vs_predicted.png
    └── 05_optimization_modes.png
```

## Simulated-data note
The dataset and optimization cost factors are simulated for academic demonstration and are not presented as real company records.

## Run
```bash
pip install pandas numpy scikit-learn matplotlib
python week4_predictive_optimization.py
```

## Limitations
A production solution should use validated historical data, time-aware validation, calibrated costs, capacity constraints, route constraints, carrier availability and uncertainty analysis.
