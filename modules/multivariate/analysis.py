import pandas as pd


def correlation_matrix(df):

    numeric = df.select_dtypes(
        include="number"
    )

    if numeric.empty:
        return pd.DataFrame()

    return numeric.corr().round(3)


def pair_plot(df):

    return df.select_dtypes(
        include="number"
    )