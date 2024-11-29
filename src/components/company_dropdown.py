from src.components import ids
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import Protocol


class CategoriesDataSource(Protocol):
    @property
    def unique_companies(self) -> list[str]: ...


def render(app: Dash, source: CategoriesDataSource) -> html.Div:
    @app.callback(
        Output(ids.COMPANY_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.QUARTER_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_COMPANIES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(year: list[str], month: list[str], _: int) -> list[str]:
        return source.unique_companies

    return html.Div(
        children=[
            html.H6("Companies"),
            dcc.Dropdown(
                id=ids.COMPANY_DROPDOWN,
                options=[
                    {"label": company, "value": company}
                    for company in source.unique_companies
                ],
                value=source.unique_companies,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_COMPANIES_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
