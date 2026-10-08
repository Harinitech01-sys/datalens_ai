import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


OUTPUT_FOLDER = "static/charts"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def create_seaborn_histogram(df, column):

    path = os.path.join(
        OUTPUT_FOLDER,
        "sns_histogram.png"
    )

    plt.figure(figsize=(10, 5))

    sns.histplot(
        df[column].dropna(),
        kde=True
    )

    plt.title(
        f"{column} Distribution"
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_seaborn_boxplot(df, column):

    path = os.path.join(
        OUTPUT_FOLDER,
        "sns_boxplot.png"
    )

    plt.figure(figsize=(10, 5))

    sns.boxplot(
        x=df[column].dropna()
    )

    plt.title(
        f"{column} Box Plot"
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_seaborn_violinplot(df, column):

    path = os.path.join(
        OUTPUT_FOLDER,
        "sns_violin.png"
    )

    plt.figure(figsize=(10, 5))

    sns.violinplot(
        x=df[column].dropna()
    )

    plt.title(
        f"{column} Violin Plot"
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_seaborn_scatterplot(df, x, y):

    path = os.path.join(
        OUTPUT_FOLDER,
        "sns_scatter.png"
    )

    plt.figure(figsize=(10, 5))

    sns.scatterplot(
        data=df,
        x=x,
        y=y
    )

    plt.title(
        f"{x} vs {y}"
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_heatmap(df):

    path = os.path.join(
        OUTPUT_FOLDER,
        "heatmap.png"
    )

    numeric = df.select_dtypes(
        include="number"
    )

    plt.figure(figsize=(11, 7))

    sns.heatmap(
        numeric.corr(),
        annot=True,
        fmt=".2f",
        linewidths=.5
    )

    plt.title(
        "Correlation Heatmap"
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")