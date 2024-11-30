from ui.components import ids
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import Protocol


class YearsDataSource(Protocol):
    @property
    def unique_years(self): ...


def render(app: Dash, source: YearsDataSource) -> html.Div:
    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return source.unique_years

    return html.Div(
        children=[
            html.H6("Years"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[
                    {"label": year, "value": year} for year in source.unique_years
                ],
                value=source.unique_years,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_YEARS_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
