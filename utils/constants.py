import os
from dotenv import load_dotenv

load_dotenv()

TAXI_DATA_URL = os.getenv("DATA_URL") or "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet"
TAXI_ZONE_LOOKUP_URL = os.getenv("TAXI_ZONE_LOOKUP_URL") or "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
TAXI_DATA_FILENAME = os.getenv("TAXI_DATA_FILENAME") or "yellow_tripdata_2026_01.parquet"
TAXI_ZONE_LOOKUP_TABLE = os.getenv("TAXI_ZONE_LOOKUP_TABLE") or "taxi_zone_lookup.csv"

CHUNK_SIZE = 8192

VALID_DATA_PATH = "data/mart/mart_cleaned/valid/valid_yellow_tripdata_2026_01.csv"
INVALID_DATA_PATH = "data/mart/mart_cleaned/invalid/invalid_yellow_tripdata_2026_01.csv"
TRANFORMED_FILE = 'transformed_yellow_tripdata_2026_01.csv'

# TRANSFORMED_FILE_PATH = '../db/transformed'