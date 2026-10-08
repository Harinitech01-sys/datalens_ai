import pandas as pd
from scipy.stats import pearsonr, spearmanr


def numeric_relationship(df, x, y):

    data = df[[x, y]].dropna()

    if len(data) < 3:
        return {"error": "Not enough data."}

    pearson = pearsonr(
        data[x],
        data[y]
    )[0]

    spearman = spearmanr(
        data[x],
        data[y]
    )[0]

    return {
        "type": "numeric",
        "x": x,
        "y": y,
        "pearson": round(pearson, 4),
        "spearman": round(spearman, 4),
        "count": len(data)
    }


def categorical_relationship(df, x, y):

    table = pd.crosstab(
        df[x],
        df[y]
    )

    return {
        "type": "categorical",
        "x": x,
        "y": y,
        "table": table.to_html(
            classes="data-table"
        )
    }


def mixed_relationship(df, numeric, categorical):

    grouped = df.groupby(
        categorical
    )[numeric].agg(
        ["count", "mean", "median", "std"]
    ).round(3)

    return {
        "type": "mixed",
        "numeric": numeric,
        "categorical": categorical,
        "table": grouped.to_html(
            classes="data-table"
        )
    }