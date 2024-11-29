from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from typing import Optional
from src.data_processor.loader import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(
        self,
        years: Optional[list[str]],
        months: Optional[list[str]],
        companies: Optional[list[str]],
    ) -> DataSource:
        if years is None:
            years = self.unique_years
        if months is None:
            months = self.unique_months
        if companies is None:
            companies = self.unique_companies

        filtered_data = self._data.query(
            "year in @years and month in @months and company in @companies"
        )
        return DataSource(filtered_data)

    def create_pivot_table(self) -> pd.DataFrame:
        pt: pd.DataFrame = self._data.pivot_table(
            values=DataSchema.NET_INCOME,
            index=[DataSchema.COMPANY],
            aggfunc="sum",
            fill_value=0,
        )
        return pt.reset_index().sort_values(DataSchema.NET_INCOME, ascending=False)

    @property
    def all_years(self) -> list[str]:
        return self._data[DataSchema.YEAR].to_list()

    @property
    def unique_years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def all_months(self) -> list[str]:
        return self._data[DataSchema.MONTH].to_list()

    @property
    def unique_months(self) -> list[str]:
        return sorted(set(self.all_months), key=int)

    @property
    def all_companies(self) -> list[str]:
        return self._data[DataSchema.COMPANY].to_list()

    @property
    def unique_companies(self) -> list[str]:
        return sorted(set(self.all_companies))

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_net_income(self) -> list[str]:
        return self._data[DataSchema.NET_INCOME].tolist()
