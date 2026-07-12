import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("data/ml_dataset.csv")

# ----------------------------
# Features
# ----------------------------

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

y = df["weight"]

# ----------------------------
# Train Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ----------------------------
# Models
# ----------------------------

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    ),
    "Extra Trees": ExtraTreesRegressor(
        n_estimators=100,
        random_state=42
    )
}

# ----------------------------
# Training Loop
# ----------------------------

results = []

for name, model in models.items():

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

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

    results.append(
        [
            name,
            round(mae, 2),
            round(mse, 2),
            round(r2, 2)
        ]
    )

# ----------------------------
# Leaderboard
# ----------------------------

results_df = pd.DataFrame(
    results,
    columns=[
        "Model",
        "MAE",
        "MSE",
        "R²"
    ]
)

results_df = results_df.sort_values(
    by="R²",
    ascending=False
)

print("\nModel Leaderboard:\n")

print(results_df)