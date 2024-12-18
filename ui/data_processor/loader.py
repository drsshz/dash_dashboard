import pandas as pd
from etl.schemas import DataSchema


def load_data(path: str) -> pd.DataFrame:
    data = pd.read_parquet(path)
    data[DataSchema.YEAR] = data[DataSchema.PERIOD].dt.year.astype(str)
    data[DataSchema.QUARTER] = data[DataSchema.PERIOD].dt.quarter.astype(str)
    return data
