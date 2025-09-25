from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


def build_figure() -> "px.Figure":
    project_root = Path(__file__).parent
    data_csv_path = project_root / "data" / "pink_morsel_sales.csv"

    data_frame = pd.read_csv(data_csv_path)
    data_frame["Date"] = pd.to_datetime(data_frame["Date"], errors="coerce")

    # Aggregate daily total sales and sort chronologically
    daily_sales = (
        data_frame.groupby("Date", as_index=False)["Sales"].sum().sort_values("Date")
    )

    figure = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time",
        labels={"Date": "Date", "Sales": "Sales ($)"},
    )

    # Mark the price increase date (2021-01-15)
    price_increase_date = pd.Timestamp("2021-01-15")
    figure.add_vline(x=price_increase_date, line_width=2, line_dash="dash", line_color="red")
    figure.add_annotation(
        x=price_increase_date,
        y=daily_sales["Sales"].max() if not daily_sales.empty else 0,
        text="Price increase\n2021-01-15",
        showarrow=True,
        yshift=20,
    )

    return figure


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            children="Pink Morsel Sales Visualiser",
            style={"textAlign": "center"},
        ),
        dcc.Graph(id="sales-line-chart", figure=build_figure()),
    ]
)


if __name__ == "__main__":
    app.run(debug=True)


