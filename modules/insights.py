def generate_insights(df):

    insights = []

    rows, columns = df.shape

    insights.append(
        f"The dataset contains {rows:,} rows and {columns} columns."
    )

    missing = int(
        df.isnull().sum().sum()
    )

    if missing == 0:
        insights.append(
            "No missing values were detected."
        )
    else:
        insights.append(
            f"The dataset contains {missing:,} missing values."
        )

    duplicates = int(
        df.duplicated().sum()
    )

    if duplicates == 0:
        insights.append(
            "No duplicate rows were detected."
        )
    else:
        insights.append(
            f"{duplicates:,} duplicate rows were detected."
        )

    numeric = df.select_dtypes(
        include="number"
    )

    for column in numeric.columns:

        skew = numeric[column].skew()

        if abs(skew) > 1:
            insights.append(
                f"{column} shows strong skewness "
                f"({skew:.2f})."
            )

    categorical = df.select_dtypes(
        include=["object", "category"]
    )

    for column in categorical.columns:

        unique = categorical[column].nunique()

        if unique <= 10:

            top = (
                categorical[column]
                .value_counts()
                .index[0]
            )

            insights.append(
                f"{column} is dominated by "
                f"the category '{top}'."
            )

    return insights