import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor

# Load dataset
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

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Train model
model = ExtraTreesRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Feature Importance
importance_df = pd.DataFrame(
    {
        "Feature": X.columns,
        "Importance": model.feature_importances_*100
    }
)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:\n")
print(importance_df)