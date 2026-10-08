import pandas as pd


def get_numeric_statistics(df):

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    statistics = pd.DataFrame({
        "Mean": numeric_df.mean(),
        "Median": numeric_df.median(),
        "Standard Deviation": numeric_df.std(),
        "Variance": numeric_df.var(),
        "Minimum": numeric_df.min(),
        "Q1": numeric_df.quantile(0.25),
        "Q2": numeric_df.quantile(0.50),
        "Q3": numeric_df.quantile(0.75),
        "Maximum": numeric_df.max()
    })

    return statistics.round(3)


def get_categorical_statistics(df):

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    rows = []

    for column in categorical_columns:

        rows.append({
            "Column": column,
            "Unique Values": df[column].nunique(),
            "Most Frequent": (
                df[column].mode().iloc[0]
                if not df[column].mode().empty
                else "-"
            ),
            "Frequency": (
                df[column].value_counts().iloc[0]
                if not df[column].value_counts().empty
                else 0
            )
        })

    return pd.DataFrame(rows)