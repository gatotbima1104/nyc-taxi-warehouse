from pathlib import Path
from scripts.extractor import TaxiExtractor
from utils.constants import (
    TAXI_DATA_FILENAME,
    TAXI_DATA_URL,
    TAXI_ZONE_LOOKUP_TABLE,
    TAXI_ZONE_LOOKUP_URL,
    POSTGRES_URL,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER
)
from scripts.database import DatabaseConnection
from scripts.loader import BronzeLoader
from scripts.schema_manager import SchemaManager

def extract() -> list[str]:
    extract_files = [
        (TAXI_DATA_URL, TAXI_DATA_FILENAME),
        (TAXI_ZONE_LOOKUP_URL, TAXI_ZONE_LOOKUP_TABLE)
    ]

    extractor = TaxiExtractor()
    downloaded_files = []

    for url, filename in extract_files:
        downloaded_files.append(
            extractor.extract(url, filename)
        )
    
    return downloaded_files

def load_to_bronze():
    connection = DatabaseConnection(
        POSTGRES_URL,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB,
        POSTGRES_USER,
        POSTGRES_PASSWORD
    )
    conn = connection.get_connection()
    
    schema = SchemaManager(conn)
    loader = BronzeLoader(conn)
    
    schema.execute_sql(Path('db/init/01_schema.sql'))
    schema.execute_sql(Path('db/init/02_bronze_load.sql'))
    
    loader.load_data(Path("data/raw/raw_yellow_tripdata_2026_01.parquet"), "raw_taxi_trips")
    loader.load_data(Path("data/raw/taxi_zone_lookup.csv"), "raw_taxi_lookup")

if __name__ == '__main__':
    extract()
    load_to_bronze()