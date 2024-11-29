from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from src.components import ids
from typing import Protocol, Optional
from src.data_processor.source import DataSource


class PieChartSource(Protocol):
    def filter(
        self,
        years: Optional[list[str]],
        months: Optional[list[str]],
        categories: Optional[list[str]],
    ) -> DataSource: ...

    @property
    def row_count(self) -> int: ...

    @property
    def all_companies(self) -> list[str]: ...

    @property
    def all_net_income(self) -> list[str]: ...


def render(app: Dash, source: PieChartSource) -> html.Div:
    @app.callback(
        Output(ids.PIE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.QUARTER_DROPDOWN, "value"),
            Input(ids.COMPANY_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
        years: list[str], months: list[str], categories: list[str]
    ) -> html.Div:
        filtered_source: PieChartSource = source.filter(years, months, categories)
        if not filtered_source.row_count:
            return html.Div("No data selected.")

        pie = go.Pie(
            labels=filtered_source.all_companies,
            values=filtered_source.all_net_income,
            hole=0.5,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")

        return html.Div(id=ids.PIE_CHART, children=[dcc.Graph(figure=fig)])

    return html.Div(id=ids.PIE_CHART)
