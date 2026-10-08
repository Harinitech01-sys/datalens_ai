import pandas as pd

from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler
)


def encode_categorical(df, columns):

    result = df.copy()

    for column in columns:

        if column in result.columns:

            result[column] = (
                result[column]
                .astype("category")
                .cat.codes
            )

    return result


def standardize_columns(df, columns):

    result = df.copy()

    valid_columns = [
        column
        for column in columns
        if column in result.columns
    ]

    if not valid_columns:
        return result

    scaler = StandardScaler()

    result[valid_columns] = scaler.fit_transform(
        result[valid_columns]
    )

    return result


def normalize_columns(df, columns):

    result = df.copy()

    valid_columns = [
        column
        for column in columns
        if column in result.columns
    ]

    if not valid_columns:
        return result

    scaler = MinMaxScaler()

    result[valid_columns] = scaler.fit_transform(
        result[valid_columns]
    )

    return result


def filter_rows(df, column, operator, value):

    result = df.copy()

    if column not in result.columns:
        return result

    try:

        numeric_value = float(value)

        if operator == ">":
            result = result[
                result[column] > numeric_value
            ]

        elif operator == "<":
            result = result[
                result[column] < numeric_value
            ]

        elif operator == ">=":
            result = result[
                result[column] >= numeric_value
            ]

        elif operator == "<=":
            result = result[
                result[column] <= numeric_value
            ]

        elif operator == "==":
            result = result[
                result[column] == numeric_value
            ]

    except ValueError:

        if operator == "==":
            result = result[
                result[column].astype(str) == value
            ]

    return result.reset_index(drop=True)


def group_and_aggregate(
    df,
    group_column,
    value_column,
    operation
):

    if (
        group_column not in df.columns
        or value_column not in df.columns
    ):
        return pd.DataFrame()

    grouped = df.groupby(group_column)[
        value_column
    ]

    if operation == "mean":
        result = grouped.mean()

    elif operation == "sum":
        result = grouped.sum()

    elif operation == "min":
        result = grouped.min()

    elif operation == "max":
        result = grouped.max()

    elif operation == "count":
        result = grouped.count()

    else:
        result = grouped.mean()

    return result.reset_index()