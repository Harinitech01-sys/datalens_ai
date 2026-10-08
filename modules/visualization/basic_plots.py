import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


OUTPUT_FOLDER = "static/charts"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def create_histogram(df, column):

    path = os.path.join(
        OUTPUT_FOLDER,
        "histogram.png"
    )

    plt.figure(figsize=(10, 5))

    plt.hist(
        df[column].dropna(),
        bins=25
    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.grid(
        alpha=0.2
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_boxplot(df, column):

    path = os.path.join(
        OUTPUT_FOLDER,
        "boxplot.png"
    )

    plt.figure(figsize=(10, 5))

    plt.boxplot(
        df[column].dropna()
    )

    plt.title(
        f"Box Plot of {column}"
    )

    plt.ylabel(column)

    plt.grid(
        alpha=0.2
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_bar_chart(df, column):

    path = os.path.join(
        OUTPUT_FOLDER,
        "bar_chart.png"
    )

    counts = (
        df[column]
        .value_counts()
        .head(15)
    )

    plt.figure(figsize=(10, 5))

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title(
        f"Distribution of {column}"
    )

    plt.xlabel(column)
    plt.ylabel("Count")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_scatter_plot(df, x, y):

    path = os.path.join(
        OUTPUT_FOLDER,
        "scatter.png"
    )

    plt.figure(figsize=(10, 5))

    plt.scatter(
        df[x],
        df[y],
        alpha=0.7
    )

    plt.title(
        f"{x} vs {y}"
    )

    plt.xlabel(x)
    plt.ylabel(y)

    plt.grid(
        alpha=0.2
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")


def create_line_plot(df, x, y):

    path = os.path.join(
        OUTPUT_FOLDER,
        "line.png"
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        df[x],
        df[y],
        linewidth=2
    )

    plt.title(
        f"{y} over {x}"
    )

    plt.xlabel(x)
    plt.ylabel(y)

    plt.grid(
        alpha=0.2
    )

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return "/" + path.replace("\\", "/")