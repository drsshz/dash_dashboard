from src.components import ids

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import Protocol


class QuartersDataSource(Protocol):
    @property
    def unique_quarters(self): ...


def render(app: Dash, source: QuartersDataSource) -> html.Div:
    @app.callback(
        Output(ids.QUARTER_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_QUARTERS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_quarters(year: list[str], _: int) -> list[str]:
        return source.unique_quarters

    return html.Div(
        children=[
            html.H6("Quarters"),
            dcc.Dropdown(
                id=ids.QUARTER_DROPDOWN,
                options=[
                    {"label": quarter, "value": quarter}
                    for quarter in source.unique_quarters
                ],
                value=source.unique_quarters,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_QUARTERS_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
