from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from ui.components import ids
from ui.data_processor.loader import DataSchema
from typing import Protocol, Optional
import pandas as pd
from ui.data_processor.source import DataSource


class BarChartSource(Protocol):
    def filter(
        self,
        years: Optional[list[str]],
        months: Optional[list[str]],
        categories: Optional[list[str]],
    ) -> DataSource: ...

    def create_pivot_table(self, indicator: str) -> pd.DataFrame: ...

    @property
    def row_count(self) -> int: ...


def render(app: Dash, source: BarChartSource) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.QUARTER_DROPDOWN, "value"),
            Input(ids.COMPANY_DROPDOWN, "value"),
            Input(ids.INDICATOR_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str], months: list[str], categories: list[str], indicator: str
    ) -> html.Div:
        filtered_source: BarChartSource = source.filter(years, months, categories)
        if not filtered_source.row_count:
            return html.Div("No data selected.")

        fig = px.bar(
            filtered_source.create_pivot_table(indicator),
            x=DataSchema.COMPANY,
            y=indicator,
            color=DataSchema.COMPANY,
        )
        return html.Div(
            id=ids.BAR_CHART,
            children=[
                html.H6(f"Bar Chart for {indicator}", className="centered-h6-heading"),
                dcc.Graph(figure=fig),
            ],
        )

    return html.Div(id=ids.BAR_CHART)
