import pandas as pd


def detect_column_types(df):

    numerical = []
    categorical = []
    datetime = []
    boolean = []

    for column in df.columns:

        series = df[column]

        if pd.api.types.is_bool_dtype(series):
            boolean.append(column)

        elif pd.api.types.is_numeric_dtype(series):
            numerical.append(column)

        elif pd.api.types.is_datetime64_any_dtype(series):
            datetime.append(column)

        else:
            converted = pd.to_datetime(
                series,
                errors="coerce"
            )

            if (
                converted.notna().mean() >= 0.8
                and series.notna().sum() > 0
            ):
                datetime.append(column)

            else:
                categorical.append(column)

    return {
        "numerical": numerical,
        "categorical": categorical,
        "datetime": datetime,
        "boolean": boolean
    }


def get_column_type_table(df):

    types = detect_column_types(df)

    rows = []

    for column in df.columns:

        if column in types["numerical"]:
            data_type = "Numerical"

        elif column in types["categorical"]:
            data_type = "Categorical"

        elif column in types["datetime"]:
            data_type = "DateTime"

        elif column in types["boolean"]:
            data_type = "Boolean"

        else:
            data_type = "Other"

        rows.append({
            "Column": column,
            "Detected Type": data_type,
            "Missing Values": int(df[column].isnull().sum()),
            "Unique Values": int(df[column].nunique())
        })

    return pd.DataFrame(rows)