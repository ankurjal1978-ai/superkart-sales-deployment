from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


REFERENCE_YEAR = 2025
RANDOM_STATE = 42
TARGET = "Product_Store_Sales_Total"
FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]
PERISHABLES = {
    "Breads",
    "Breakfast",
    "Dairy",
    "Fruits and Vegetables",
    "Meat",
    "Seafood",
}


data = pd.read_csv(Path(__file__).with_name("SuperKart.csv"))
data["Product_Sugar_Content"] = data["Product_Sugar_Content"].replace({"reg": "Regular"})
data["Product_Id_char"] = data["Product_Id"].str[:2]
data["Store_Age_Years"] = REFERENCE_YEAR - data["Store_Establishment_Year"]
data["Product_Type_Category"] = np.where(
    data["Product_Type"].isin(PERISHABLES),
    "Perishables",
    "Non Perishables",
)

X = data[FEATURES]
y = data[TARGET]
numeric_features = X.select_dtypes(exclude="object").columns.tolist()
categorical_features = X.select_dtypes(include="object").columns.tolist()

preprocessor = ColumnTransformer(
    [
        ("numeric", "passthrough", numeric_features),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            categorical_features,
        ),
    ],
    verbose_feature_names_out=False,
)

model = Pipeline(
    [
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=300,
                max_depth=None,
                max_features=0.8,
                min_samples_leaf=3,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        ),
    ]
)
model.fit(X, y)
joblib.dump(model, Path(__file__).with_name("superkart_model.joblib"))
print(f"Trained deployment pipeline on {len(data):,} rows.")
