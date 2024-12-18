from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from ui.components import ids
from typing import Protocol, Optional
from ui.data_processor.source import DataSource


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
    def all_net_income(self) -> list[float]: ...

    @property
    def all_revenue(self) -> list[float]: ...

    @property
    def all_assets(self) -> list[float]: ...

    @property
    def all_liabilities(self) -> list[float]: ...


def render(app: Dash, source: PieChartSource) -> html.Div:
    @app.callback(
        Output(ids.PIE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.QUARTER_DROPDOWN, "value"),
            Input(ids.COMPANY_DROPDOWN, "value"),
            Input(ids.INDICATOR_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
        years: list[str], months: list[str], categories: list[str], indicator: str
    ) -> html.Div:
        filtered_source: PieChartSource = source.filter(years, months, categories)
        if not filtered_source.row_count:
            return html.Div("No data selected.")

        pie = go.Pie(
            labels=filtered_source.all_companies,
            values=getattr(filtered_source, f"all_{indicator}"),
            hole=0.5,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")

        return html.Div(
            id=ids.PIE_CHART,
            children=[
                html.H6(f"Pie Chart for {indicator}", className="centered-h6-heading"),
                dcc.Graph(figure=fig),
            ],
        )

    return html.Div(id=ids.PIE_CHART)
