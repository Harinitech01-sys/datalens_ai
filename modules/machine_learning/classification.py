import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def run_classification(
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

    if data[target].nunique() < 2:
        return {
            "error": "Target must contain at least two classes."
        }

    X = data[features]

    y = data[target]

    for column in X.select_dtypes(
        include=["object", "category"]
    ).columns:

        X = X.copy()

        X[column] = LabelEncoder().fit_transform(
            X[column].astype(str)
        )

    if y.dtype == "object" or str(y.dtype) == "category":

        encoder = LabelEncoder()

        y = encoder.fit_transform(
            y.astype(str)
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000
        ),
        "Decision Tree": DecisionTreeClassifier(
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
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

        results.append({
            "Model": name,
            "Accuracy": round(
                accuracy_score(
                    y_test,
                    prediction
                ),
                4
            ),
            "Precision": round(
                precision_score(
                    y_test,
                    prediction,
                    average="weighted",
                    zero_division=0
                ),
                4
            ),
            "Recall": round(
                recall_score(
                    y_test,
                    prediction,
                    average="weighted",
                    zero_division=0
                ),
                4
            ),
            "F1 Score": round(
                f1_score(
                    y_test,
                    prediction,
                    average="weighted",
                    zero_division=0
                ),
                4
            )
        })

    return {
        "type": "classification",
        "results": pd.DataFrame(
            results
        ).to_html(
            classes="data-table",
            index=False
        )
    }