import pandas as pd


def get_distribution_analysis(df, column):

    if column not in df.columns:
        return {}

    series = pd.to_numeric(df[column], errors="coerce").dropna()

    if series.empty:
        return {}

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[
        (series < lower_bound) |
        (series > upper_bound)
    ]

    return {
        "column": column,
        "count": int(series.count()),
        "mean": round(series.mean(), 3),
        "median": round(series.median(), 3),
        "std": round(series.std(), 3),
        "skewness": round(series.skew(), 3),
        "q1": round(q1, 3),
        "q2": round(series.median(), 3),
        "q3": round(q3, 3),
        "iqr": round(iqr, 3),
        "lower_bound": round(lower_bound, 3),
        "upper_bound": round(upper_bound, 3),
        "outlier_count": int(len(outliers)),
        "outlier_percentage": round(
            (len(outliers) / len(series)) * 100,
            2
        )
    }