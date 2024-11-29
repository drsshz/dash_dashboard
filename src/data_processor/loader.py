import pandas as pd
from data.schemas import DataSchema


def load_data(path: str) -> pd.DataFrame:
    data = pd.read_parquet(path)
    data[DataSchema.YEAR] = data[DataSchema.PERIOD].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.PERIOD].dt.month.astype(str)
    return data
