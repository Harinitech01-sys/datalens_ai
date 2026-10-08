import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(df, filename):

    folder = "outputs/reports"

    os.makedirs(
        folder,
        exist_ok=True
    )

    path = os.path.join(
        folder,
        "DataLens_Report.pdf"
    )

    document = SimpleDocTemplate(
        path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "DataLens — Data Exploration Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            f"Dataset: {filename}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Rows: {df.shape[0]}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Columns: {df.shape[1]}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    numeric = df.describe().round(3)

    data = [
        ["Statistic"] +
        numeric.columns.tolist()
    ]

    for index, row in numeric.iterrows():

        data.append(
            [index] +
            row.tolist()
        )

    table = Table(data)

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#111827")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(table)

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Conclusion",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "The dataset was explored using profiling, "
            "data preparation, statistical analysis, "
            "visualization and machine learning techniques.",
            styles["Normal"]
        )
    )

    document.build(story)

    return path