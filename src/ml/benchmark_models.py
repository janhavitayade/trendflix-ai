import os
import joblib
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

FEATURE_COLUMNS = [
    "rating",
    "status_encoded",
    "premiered_year",
    "averageRuntime",
    "genre_count",
    "show_age"
]

X = df[FEATURE_COLUMNS]

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
trained_models = {}

for name, model in models.items():

    model.fit(
        X_train,
        y_train
    )

    trained_models[name] = model

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

# ----------------------------
# NEW: Persist the production model
# ----------------------------
# WHY: benchmark_models.py used to just print a leaderboard and throw
# every trained model away when the script exited. The Streamlit app
# needs an actual fitted model object on disk to make live predictions
# from user input on the new "Predict" page — so we save the Extra
# Trees Regressor (the model already selected as production, per the
# app's own "Production Model" section) as a .pkl file with joblib.
#
# We also save FEATURE_COLUMNS alongside the model. This guarantees
# the app always builds its prediction input in the exact same column
# order the model was trained on, even if this list is edited later.

os.makedirs("models", exist_ok=True)

BEST_MODEL_NAME = "Extra Trees"

joblib.dump(
    trained_models[BEST_MODEL_NAME],
    "models/extra_trees_model.pkl"
)

joblib.dump(
    FEATURE_COLUMNS,
    "models/feature_columns.pkl"
)

print(f"\nSaved production model '{BEST_MODEL_NAME}' -> models/extra_trees_model.pkl")
print("Saved feature column order -> models/feature_columns.pkl")