from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from etl.etl_pipeline import run_etl_pipeline
from src.components.layout import create_layout
from src.data_processor.source import DataSource
from src.data_processor.loader import load_data
from pathlib import Path
from loguru import logger


DATASET = "willianoliveiragibin/top-12-german-companies"
DASH_DATA_PATH = Path(__file__).parent / "data" / "processed" / "dash_data.parquet"


def run_dash_app(data_path: Path) -> None:
    data = load_data(data_path)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Financial dashboard of Top German companies"
    app.layout = create_layout(app, DataSource(data))
    app.run()


if __name__ == "__main__":
    logger.info("Running the ETL pipeline to fetch the data...")
    run_etl_pipeline(DATASET, DASH_DATA_PATH)
    logger.info("ETL pipeline finished!")
    logger.info("Starting the financial dashboard of top german companies...")
    run_dash_app(DASH_DATA_PATH)
