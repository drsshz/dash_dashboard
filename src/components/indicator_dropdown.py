from src.components import ids
from dash import Dash, html, dcc
from typing import Protocol


class IndicatorsDataSource(Protocol):
    @property
    def unique_indicators(self): ...


def render(_: Dash, source: IndicatorsDataSource) -> html.Div:
    return html.Div(
        children=[
            html.H6("Indicators"),
            dcc.Dropdown(
                id=ids.INDICATOR_DROPDOWN,
                options=[
                    {"label": indicator, "value": indicator}
                    for indicator in source.unique_indicators
                ],
                value=source.unique_indicators[0],
                multi=False,
            ),
        ]
    )
