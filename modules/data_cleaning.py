import pandas as pd


def get_quality_report(df):

    total_cells = df.shape[0] * df.shape[1]

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    missing_percentage = 0

    if total_cells > 0:
        missing_percentage = round(
            (missing_values / total_cells) * 100,
            2
        )

    duplicate_percentage = 0

    if len(df) > 0:
        duplicate_percentage = round(
            (duplicate_rows / len(df)) * 100,
            2
        )

    return {
        "total_cells": total_cells,
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": duplicate_percentage
    }


def remove_duplicates(df):

    return df.drop_duplicates().reset_index(drop=True)


def fill_missing_mean(df, columns):

    result = df.copy()

    for column in columns:

        if pd.api.types.is_numeric_dtype(
            result[column]
        ):

            result[column] = result[column].fillna(
                result[column].mean()
            )

    return result


def fill_missing_median(df, columns):

    result = df.copy()

    for column in columns:

        if pd.api.types.is_numeric_dtype(
            result[column]
        ):

            result[column] = result[column].fillna(
                result[column].median()
            )

    return result


def fill_missing_mode(df, columns):

    result = df.copy()

    for column in columns:

        if result[column].isnull().any():

            mode = result[column].mode()

            if not mode.empty:

                result[column] = result[column].fillna(
                    mode.iloc[0]
                )

    return result


def drop_missing_rows(df):

    return df.dropna().reset_index(drop=True)