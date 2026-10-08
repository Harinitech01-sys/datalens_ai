from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource


def create_bokeh_scatter(
    df,
    x_column,
    y_column
):

    data = df[
        [x_column, y_column]
    ].dropna()

    source = ColumnDataSource(
        data
    )

    plot = figure(
        title=f"{x_column} vs {y_column}",
        x_axis_label=x_column,
        y_axis_label=y_column,
        width=950,
        height=500,
        tools="pan,wheel_zoom,box_zoom,reset,save,hover"
    )

    plot.scatter(
        x=x_column,
        y=y_column,
        source=source,
        size=9,
        alpha=0.7
    )

    script, div = components(
        plot
    )

    return script, div