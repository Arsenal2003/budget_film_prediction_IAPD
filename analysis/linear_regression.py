import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

file_path = '../data/movies_with_roi_features.csv'
df = pd.read_csv(file_path)

df["ROI"] = np.log1p(df["ROI"])

X = df.drop(columns=["ROI", "Gross Worldwide", "Title", "Budget", "URL"])
y = df["ROI"]

numeric_features = ["Rating", "Popularity", "Runtime_minutes"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features)
    ]
)

model = LinearRegression()

pipeline = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", model)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
print("R2 score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
