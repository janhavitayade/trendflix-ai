import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load dataset

df = pd.read_csv(
    "data/ml_dataset.csv"
)

# Features

X = df[
    [
        "rating",
        "status_encoded",
        "premiered_year",
        "averageRuntime",
        "genre_count",
        "show_age"
    ]
]

# Target

y = df["weight"]

# Train/Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Model

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# Predictions

predictions = model.predict(
    X_test
)

# Metrics

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("Random Forest Results:\n")

print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("R²:", round(r2, 2))