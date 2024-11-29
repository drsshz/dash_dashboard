import pandas as pd
import kagglehub
from loguru import logger
from pathlib import Path
from data.schemas import DataSchemaRaw, DataSchema

DATASET = "willianoliveiragibin/top-12-german-companies"
OUTPUT_DIR = Path("data") / "processed"
output_path_NAME = "dash_data.parquet"


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    column_renames = {
        getattr(DataSchemaRaw, attr): getattr(DataSchema, attr)
        for attr in dir(DataSchemaRaw)
        if not attr.startswith("__") and hasattr(DataSchema, attr)
    }
    return df.rename(columns=column_renames, inplace=False)


def extract_data(dataset_name: str) -> str:
    logger.info(f"Downloading dataset: {dataset_name}")
    dataset_path = kagglehub.dataset_download(dataset_name)
    logger.info(f"Dataset downloaded to: {dataset_path}")
    return dataset_path


def transform_data(dataset_path: str) -> pd.DataFrame:
    logger.info(f"Transforming data in {dataset_path}")
    csv_files = [file for file in Path(dataset_path).iterdir() if file.suffix == ".csv"]
    if not csv_files:
        raise Exception("No CSV files found in the dataset folder.")
    csv_file_path = Path(dataset_path) / csv_files[0]
    df = pd.read_csv(
        csv_file_path,
        usecols=[DataSchemaRaw.COMPANY, DataSchemaRaw.NET_INCOME, DataSchemaRaw.PERIOD],
        dtype={
            DataSchemaRaw.COMPANY: str,
            DataSchemaRaw.NET_INCOME: float,
        },
        parse_dates=[DataSchemaRaw.PERIOD],
    )
    df = rename_columns(df)
    logger.info("Columns renamed.")
    initial_row_count = len(df)
    df.dropna(inplace=True)
    final_row_count = len(df)
    logger.info(f"Removed {initial_row_count - final_row_count} rows with null values.")
    return df


def load_data(df: pd.DataFrame, output_path: Path) -> None:
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"Transformed data saved to {output_path}")


def run_etl_pipeline(dataset: str, output_path: Path) -> None:
    dataset_path = extract_data(dataset)
    processed_data = transform_data(dataset_path)
    load_data(processed_data, output_path)
