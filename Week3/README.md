Week 3 – Advanced Data Analysis and Visualization in Logistics

#Objective

This Week 3 project performs exploratory data analysis (EDA) and visualization on a simulated logistics dataset. It extends the Week 2 preprocessing work and focuses on distributions, central tendency, correlations, operational comparisons, and visual communication of logistics KPIs.

Important data note

The dataset in this folder is a simulated demonstration dataset created for the assignment. It is not presented as a direct extract from a company's operational system.

Files

Week3/
├── week3_analysis.py
├── week3_logistics_analysis_data.csv
├── summary_statistics.csv
├── correlation_matrix.csv
├── traffic_kpi_summary.csv
├── charts/
│   ├── 01_delivery_distribution.png
│   ├── 02_distance_vs_cost.png
│   ├── 03_traffic_delivery.png
│   ├── 04_delay_by_traffic.png
│   └── 05_correlation_matrix.png
└── README.md



Analysis performed



1. Descriptive statistics

Mean, median, standard deviation, quartiles, minimum and maximum values are calculated for distance, shipment weight, actual delivery time, fuel consumption, transportation cost and delay.

2. Delivery-time distribution

A histogram is used to identify the typical delivery-time range and whether unusually long delivery durations occur.

3. Transportation cost analysis

A scatter plot compares distance with transportation cost. This helps examine whether longer routes are associated with higher logistics expenditure.

4. Traffic analysis

Average delivery time, average delay, late-delivery rate and transportation cost are compared across Low, Medium and High traffic conditions.

5. Delay analysis

A box plot compares delay distributions across traffic levels, making differences in spread and extreme delays easier to identify.

6. Correlation analysis

A correlation matrix is calculated to examine linear relationships among operational variables.

Key simulated findings

Because this is a simulated dataset, the following findings describe the generated sample rather than real-world performance:





Higher traffic levels are associated with higher average delivery times in the simulation.



Transportation cost generally increases with delivery distance.



Delivery delays vary more under high-traffic conditions.



Distance and fuel usage show a positive relationship because fuel is generated from route distance.



Transportation cost is influenced by both distance and shipment characteristics.

These observations are descriptive associations, not proof of causation.

Why the visualizations matter

Each visualization answers a different logistics question:







Visualization



Business question





Histogram



What is the normal delivery-time pattern?





Scatter plot



How does distance relate to transportation cost?





Bar chart



How does traffic condition relate to average delivery time?





Box plot



How variable are delivery delays under different traffic conditions?





Correlation matrix



Which numeric variables move together?



Run the project

Install:

pip install pandas numpy matplotlib

Run:

python week3_analysis.py

The script regenerates the summary tables and chart images.

Connection to Week 1 and Week 2

Week 1 defined logistics KPIs and the analytical roadmap.

Week 2 prepared and validated logistics data.

Week 3 uses that prepared structure to perform EDA and visualization. The resulting insights can later support regression, clustering and optimization.

Limitations

The sample is simulated. Correlation does not establish causation, and the results should not be interpreted as actual company performance. A production analysis should use validated operational records and include additional dimensions such as geography, carrier, warehouse, seasonality and service-level agreements.
