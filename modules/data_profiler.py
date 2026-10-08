import pandas as pd


def get_dataset_info(df):

    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(
            df.isnull().sum().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
        "total_values": int(
            df.size
        )
    }

    return info


def get_column_info(df):

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    return column_info