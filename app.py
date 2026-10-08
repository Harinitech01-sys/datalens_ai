import os

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file

from modules.data_profiler import (
    get_dataset_info,
    get_column_info
)

from modules.column_detector import (
    detect_column_types
)

from modules.data_cleaning import (
    get_quality_report,
    remove_duplicates,
    fill_missing_mean,
    fill_missing_median,
    fill_missing_mode,
    drop_missing_rows
)

from modules.data_transformation import (
    encode_categorical,
    standardize_columns,
    normalize_columns,
    filter_rows,
    group_and_aggregate
)

from modules.visualization.basic_plots import (
    create_histogram,
    create_boxplot,
    create_bar_chart,
    create_scatter_plot,
    create_line_plot
)

from modules.visualization.seaborn_plots import (
    create_seaborn_histogram,
    create_seaborn_boxplot,
    create_seaborn_violinplot,
    create_seaborn_scatterplot,
    create_heatmap
)

from modules.visualization.bokeh_plots import (
    create_bokeh_scatter
)

from modules.statistics.descriptive import (
    get_numeric_statistics,
    get_categorical_statistics
)

from modules.statistics.distribution import (
    get_distribution_analysis
)

from modules.relationships.analysis import (
    numeric_relationship,
    categorical_relationship,
    mixed_relationship
)

from modules.multivariate.analysis import (
    correlation_matrix,
    pair_plot
)

from modules.dimensionality.pca import (
    perform_pca
)

from modules.machine_learning.classification import (
    run_classification
)

from modules.machine_learning.regression import (
    run_regression
)

from modules.insights import (
    generate_insights
)

from modules.report_generator import (
    generate_report
)


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


UPLOAD_FOLDER = "data/uploads"
REPORT_FOLDER = "outputs/reports"
CHART_FOLDER = "static/charts"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)


df = None
filename = None


def load_uploaded_file(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".csv":
        return pd.read_csv(filepath)

    if extension == ".xlsx":
        return pd.read_excel(filepath)

    raise ValueError("Only CSV and XLSX files are supported.")


def dataset_loaded():
    return df is not None and not df.empty


def common_context():
    if not dataset_loaded():
        return {
            "filename": filename,
            "info": None,
            "quality": None,
            "types": {
                "numerical": [],
                "categorical": [],
                "datetime": [],
                "boolean": []
            },
            "columns": []
        }

    types = detect_column_types(df)

    return {
        "filename": filename,
        "info": get_dataset_info(df),
        "quality": get_quality_report(df),
        "types": types,
        "columns": list(df.columns)
    }


@app.route("/")
def home():
    context = common_context()

    return render_template(
        "index.html",
        **context
    )


@app.route("/upload", methods=["POST"])
def upload():

    global df
    global filename

    file = request.files.get("dataset")

    if file is None or file.filename == "":
        return redirect(url_for("home"))

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".csv", ".xlsx"]:
        return render_template(
            "index.html",
            error="Please upload a CSV or XLSX file.",
            **common_context()
        )

    safe_name = os.path.basename(file.filename)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        safe_name
    )

    file.save(filepath)

    try:
        df = load_uploaded_file(filepath)
        filename = safe_name

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return redirect(url_for("dataset"))

    except Exception as error:

        df = None
        filename = None

        return render_template(
            "index.html",
            error=f"Unable to read dataset: {error}",
            **common_context()
        )


@app.route("/dataset")
def dataset():

    context = common_context()

    preview = None
    column_info = None

    if dataset_loaded():

        preview = df.head(10).to_html(
            classes="data-table",
            index=False
        )

        column_info = get_column_info(df).to_html(
            classes="data-table",
            index=False
        )

    return render_template(
        "dataset.html",
        **context,
        preview=preview,
        column_info=column_info
    )


@app.route("/profiling")
def profiling():

    context = common_context()

    column_info = None

    if dataset_loaded():

        column_info = get_column_info(df).to_html(
            classes="data-table",
            index=False
        )

    return render_template(
        "profiling.html",
        **context,
        column_info=column_info
    )


@app.route("/preparation", methods=["GET", "POST"])
def preparation():

    context = common_context()

    result = None

    if dataset_loaded() and request.method == "POST":

        action = request.form.get("action")

        try:

            if action == "duplicates":

                cleaned = remove_duplicates(df)

                result = {
                    "title": "Duplicate Removal",
                    "message":
                        f"Removed {len(df) - len(cleaned)} duplicate rows."
                }

            elif action == "mean":

                columns = request.form.getlist("columns")

                cleaned = fill_missing_mean(
                    df,
                    columns
                )

                result = {
                    "title": "Mean Imputation",
                    "message":
                        "Missing numerical values were filled using mean values."
                }

            elif action == "median":

                columns = request.form.getlist("columns")

                cleaned = fill_missing_median(
                    df,
                    columns
                )

                result = {
                    "title": "Median Imputation",
                    "message":
                        "Missing numerical values were filled using median values."
                }

            elif action == "mode":

                columns = request.form.getlist("columns")

                cleaned = fill_missing_mode(
                    df,
                    columns
                )

                result = {
                    "title": "Mode Imputation",
                    "message":
                        "Missing values were filled using mode values."
                }

            elif action == "drop_missing":

                cleaned = drop_missing_rows(df)

                result = {
                    "title": "Missing Rows Removed",
                    "message":
                        f"Removed {len(df) - len(cleaned)} rows."
                }

        except Exception as error:

            result = {
                "title": "Preparation Error",
                "message": str(error)
            }

    return render_template(
        "preparation.html",
        **context,
        numerical=context["types"]["numerical"],
        categorical=context["types"]["categorical"],
        result=result
    )


@app.route("/visualize", methods=["GET", "POST"])
def visualize():

    context = common_context()

    chart = None
    chart_title = None
    error = None

    if dataset_loaded() and request.method == "POST":

        chart_type = request.form.get("chart_type")
        column = request.form.get("column")
        x = request.form.get("x")
        y = request.form.get("y")

        try:

            if chart_type == "histogram":

                chart = create_histogram(
                    df,
                    column
                )

                chart_title = f"Histogram — {column}"

            elif chart_type == "boxplot":

                chart = create_boxplot(
                    df,
                    column
                )

                chart_title = f"Box Plot — {column}"

            elif chart_type == "bar":

                chart = create_bar_chart(
                    df,
                    column
                )

                chart_title = f"Bar Chart — {column}"

            elif chart_type == "scatter":

                chart = create_scatter_plot(
                    df,
                    x,
                    y
                )

                chart_title = f"{x} vs {y}"

            elif chart_type == "line":

                chart = create_line_plot(
                    df,
                    x,
                    y
                )

                chart_title = f"{y} over {x}"

        except Exception as exception:

            error = str(exception)

    return render_template(
        "visualize.html",
        **context,
        columns=context["columns"],
        numerical=context["types"]["numerical"],
        chart=chart,
        chart_title=chart_title,
        error=error
    )


@app.route("/seaborn", methods=["GET", "POST"])
def seaborn():

    context = common_context()

    chart = None

    if dataset_loaded() and request.method == "POST":

        chart_type = request.form.get("chart_type")
        column = request.form.get("column")
        x = request.form.get("x")
        y = request.form.get("y")

        try:

            if chart_type == "histogram":

                chart = create_seaborn_histogram(
                    df,
                    column
                )

            elif chart_type == "boxplot":

                chart = create_seaborn_boxplot(
                    df,
                    column
                )

            elif chart_type == "violin":

                chart = create_seaborn_violinplot(
                    df,
                    column
                )

            elif chart_type == "scatter":

                chart = create_seaborn_scatterplot(
                    df,
                    x,
                    y
                )

            elif chart_type == "heatmap":

                chart = create_heatmap(df)

        except Exception as exception:

            return render_template(
                "visualize.html",
                **context,
                chart=None,
                error=str(exception)
            )

    return render_template(
        "visualize.html",
        **context,
        chart=chart
    )


@app.route("/statistics")
def statistics():

    context = common_context()

    numeric = None
    categorical = None

    if dataset_loaded():

        numeric = get_numeric_statistics(
            df
        ).to_html(
            classes="data-table"
        )

        categorical = get_categorical_statistics(
            df
        ).to_html(
            classes="data-table",
            index=False
        )

    return render_template(
        "statistics.html",
        **context,
        numeric=numeric,
        categorical=categorical
    )


@app.route("/distribution", methods=["GET", "POST"])
def distribution():

    context = common_context()

    result = None

    if dataset_loaded() and request.method == "POST":

        column = request.form.get("column")

        result = get_distribution_analysis(
            df,
            column
        )

    return render_template(
        "statistics.html",
        **context,
        distribution=result
    )


@app.route("/relationships", methods=["GET", "POST"])
def relationships():

    context = common_context()

    result = None

    if dataset_loaded() and request.method == "POST":

        relationship_type = request.form.get(
            "relationship_type"
        )

        try:

            if relationship_type == "numeric":

                x = request.form.get("x")
                y = request.form.get("y")

                result = numeric_relationship(
                    df,
                    x,
                    y
                )

            elif relationship_type == "categorical":

                x = request.form.get("x")
                y = request.form.get("y")

                result = categorical_relationship(
                    df,
                    x,
                    y
                )

            elif relationship_type == "mixed":

                numeric = request.form.get("numeric")
                categorical = request.form.get("categorical")

                result = mixed_relationship(
                    df,
                    numeric,
                    categorical
                )

        except Exception as exception:

            result = {
                "error": str(exception)
            }

    return render_template(
        "relationships.html",
        **context,
        numerical=context["types"]["numerical"],
        categorical=context["types"]["categorical"],
        result=result
    )


@app.route("/multivariate", methods=["GET", "POST"])
def multivariate():

    context = common_context()

    matrix = None

    if dataset_loaded():

        matrix = correlation_matrix(
            df
        ).to_html(
            classes="data-table"
        )

    return render_template(
        "multivariate.html",
        **context,
        numerical=context["types"]["numerical"],
        matrix=matrix
    )


@app.route("/bokeh", methods=["GET", "POST"])
def bokeh():

    context = common_context()

    script = None
    div = None
    error = None

    if dataset_loaded() and request.method == "POST":

        x = request.form.get("x")
        y = request.form.get("y")

        try:

            script, div = create_bokeh_scatter(
                df,
                x,
                y
            )

        except Exception as exception:

            error = str(exception)

    return render_template(
        "multivariate.html",
        **context,
        numerical=context["types"]["numerical"],
        matrix=None,
        bokeh_script=script,
        bokeh_div=div,
        error=error
    )


@app.route("/pca", methods=["GET", "POST"])
def pca():

    context = common_context()

    result = None

    if dataset_loaded() and request.method == "POST":

        columns = request.form.getlist(
            "columns"
        )

        result = perform_pca(
            df,
            columns
        )

    return render_template(
        "dimensionality.html",
        **context,
        numerical=context["types"]["numerical"],
        result=result
    )


@app.route("/machine-learning", methods=["GET", "POST"])
def machine_learning():

    context = common_context()

    result = None

    if dataset_loaded() and request.method == "POST":

        model_type = request.form.get(
            "model_type"
        )

        target = request.form.get(
            "target"
        )

        features = request.form.getlist(
            "features"
        )

        try:

            if model_type == "classification":

                result = run_classification(
                    df,
                    features,
                    target
                )

            elif model_type == "regression":

                result = run_regression(
                    df,
                    features,
                    target
                )

        except Exception as exception:

            result = {
                "error": str(exception)
            }

    return render_template(
        "machine_learning.html",
        **context,
        numerical=context["types"]["numerical"],
        categorical=context["types"]["categorical"],
        result=result
    )


@app.route("/insights")
def insights():

    context = common_context()

    generated = []

    if dataset_loaded():

        generated = generate_insights(
            df
        )

    return render_template(
        "insights.html",
        **context,
        insights=generated
    )


@app.route("/report")
def report():

    context = common_context()

    numeric = None
    generated = []

    if dataset_loaded():

        numeric = get_numeric_statistics(
            df
        ).to_html(
            classes="data-table"
        )

        generated = generate_insights(
            df
        )

    return render_template(
        "report.html",
        **context,
        filename=filename,
        rows=context["info"]["rows"] if context["info"] else 0,
        columns=context["info"]["columns"] if context["info"] else 0,
        numeric=numeric,
        insights=generated
    )


@app.route("/download-report")
def download_report():

    if not dataset_loaded():

        return redirect(
            url_for("home")
        )

    report_path = generate_report(
        df,
        filename
    )

    return send_file(
        report_path,
        as_attachment=True,
        download_name="DataLens_Report.pdf"
    )


@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum size is 50 MB.",
        **common_context()
    ), 413


@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "index.html",
        error="The requested page could not be found.",
        **common_context()
    ), 404


@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "index.html",
        error="Something went wrong while processing the request.",
        **common_context()
    ), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )