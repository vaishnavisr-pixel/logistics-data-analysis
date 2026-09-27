# Week 4 predictive modeling and optimization
from pathlib import Path
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE=Path(__file__).resolve().parent
df=pd.read_csv(BASE/"week3_logistics_analysis_data.csv")
features=["Distance_km","Order_Weight_kg","Delivery_Days_Scheduled","Fuel_Used_L","Traffic_Level","Shipping_Mode"]
num=["Distance_km","Order_Weight_kg","Delivery_Days_Scheduled","Fuel_Used_L"]; cat=["Traffic_Level","Shipping_Mode"]
pre=ColumnTransformer([("num",StandardScaler(),num),("cat",OneHotEncoder(handle_unknown="ignore"),cat)])
X=df[features]; y=df["Delivery_Days_Actual"]
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)

models={
"Linear Regression":Pipeline([("pre",pre),("model",LinearRegression())]),
"Random Forest":Pipeline([("pre",pre),("model",RandomForestRegressor(n_estimators=250,max_depth=10,min_samples_leaf=2,random_state=42))])
}
for name,model in models.items():
    model.fit(Xtr,ytr)
    p=model.predict(Xte)
    print(name, "MAE", mean_absolute_error(yte,p), "RMSE", mean_squared_error(yte,p)**.5, "R2", r2_score(yte,p))

cv=KFold(n_splits=5,shuffle=True,random_state=42)
cv_mae=-cross_val_score(models["Random Forest"],Xtr,ytr,cv=cv,scoring="neg_mean_absolute_error")
print("5-fold CV MAE:",cv_mae.mean())

grid=GridSearchCV(
    Pipeline([("pre",pre),("model",RandomForestRegressor(random_state=42))]),
    {"model__n_estimators":[150,250],"model__max_depth":[8,10,None],"model__min_samples_leaf":[1,2]},
    cv=3,scoring="neg_mean_absolute_error"
)
grid.fit(Xtr,ytr)
print("Best parameters:",grid.best_params_)

# A production implementation can enumerate feasible shipping modes,
# calculate predicted SLA performance and choose the minimum-cost feasible option.
