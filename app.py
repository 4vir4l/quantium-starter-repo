from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback


def build_figure(region: str | None = None) -> "px.Figure":
    project_root = Path(__file__).parent
    data_csv_path = project_root / "data" / "pink_morsel_sales.csv"

    data_frame = pd.read_csv(data_csv_path)
    data_frame["Date"] = pd.to_datetime(data_frame["Date"], errors="coerce")

    # Optional filter by region (except for "all")
    if region and region.lower() != "all":
        data_frame = data_frame[data_frame["Region"].str.lower() == region.lower()]

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

region_options = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]

app.layout = html.Div(
    children=[
        html.H1(
            children="Pink Morsel Sales Visualiser",
            style={"textAlign": "center"},
        ),
        html.Div(
            children=[
                html.Label("Region", htmlFor="region-radio"),
                dcc.RadioItems(
                    id="region-radio",
                    options=region_options,
                    value="all",
                    labelStyle={"display": "inline-block", "marginRight": "12px"},
                    inline=True,
                ),
            ],
            style={"textAlign": "center", "margin": "16px 0"},
        ),
        dcc.Graph(id="sales-line-chart", figure=build_figure("all")),
    ]
)


@callback(Output("sales-line-chart", "figure"), Input("region-radio", "value"))
def update_chart(selected_region: str):
    return build_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)


