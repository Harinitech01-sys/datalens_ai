import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


def run_regression(
    df,
    features,
    target
):

    if not features:
        return {
            "error": "Select at least one feature."
        }

    data = df[
        features + [target]
    ].dropna()

    X = data[features]

    y = data[target]

    for column in X.select_dtypes(
        include=["object", "category"]
    ).columns:

        X = X.copy()

        X[column] = LabelEncoder().fit_transform(
            X[column].astype(str)
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),

        "Decision Tree": DecisionTreeRegressor(
            random_state=42
        ),

        "Random Forest": RandomForestRegressor(
            random_state=42,
            n_estimators=100
        )
    }

    results = []

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        prediction = model.predict(
            X_test
        )

        mse = mean_squared_error(
            y_test,
            prediction
        )

        results.append({
            "Model": name,
            "MAE": round(
                mean_absolute_error(
                    y_test,
                    prediction
                ),
                4
            ),
            "MSE": round(
                mse,
                4
            ),
            "RMSE": round(
                np.sqrt(mse),
                4
            ),
            "R2 Score": round(
                r2_score(
                    y_test,
                    prediction
                ),
                4
            )
        })

    return {
        "type": "regression",
        "results": pd.DataFrame(
            results
        ).to_html(
            classes="data-table",
            index=False
        )
    }