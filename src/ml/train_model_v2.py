import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load Dataset V2
df = pd.read_csv("data/ml_dataset.csv")

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
    test_size=0.2,
    random_state=42
)

# Model
model = LinearRegression()

# Train
model.fit(X_train, y_train)

print("Model V2 trained successfully!")

# Predictions
predictions = model.predict(X_test)

print("\nFirst 10 Predictions:\n")

for actual, predicted in zip(y_test[:10], predictions[:10]):
    print(
        f"Actual: {actual} | Predicted: {predicted:.2f}"
    )

# Evaluation
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Evaluation:\n")

print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("R² Score:", round(r2, 2))