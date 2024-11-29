from src.components import ids

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import Protocol


class MonthsDataSource(Protocol):
    @property
    def unique_months(self): ...


def render(app: Dash, source: MonthsDataSource) -> html.Div:
    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_months(year: list[str], _: int) -> list[str]:
        return source.unique_months

    return html.Div(
        children=[
            html.H6("Months"),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[
                    {"label": month, "value": month} for month in source.unique_months
                ],
                value=source.unique_months,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
