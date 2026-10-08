import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def perform_pca(df, columns):

    if len(columns) < 2:
        return {
            "error": "Select at least two numerical columns."
        }

    data = df[columns].dropna()

    if len(data) < 2:
        return {
            "error": "Not enough valid rows."
        }

    scaler = StandardScaler()

    scaled = scaler.fit_transform(data)

    components = min(
        3,
        len(columns)
    )

    pca = PCA(
        n_components=components
    )

    transformed = pca.fit_transform(
        scaled
    )

    result = pd.DataFrame(
        transformed,
        columns=[
            f"PC{i + 1}"
            for i in range(components)
        ]
    )

    return {
        "components": result.to_html(
            classes="data-table",
            index=False
        ),
        "explained_variance": [
            round(x, 4)
            for x in pca.explained_variance_ratio_
        ],
        "total_variance": round(
            pca.explained_variance_ratio_.sum(),
            4
        )
    }