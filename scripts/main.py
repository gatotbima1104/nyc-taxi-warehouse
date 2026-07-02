from pathlib import Path
from datetime import datetime

from scripts.taxi_extractor import TaxiExtractor
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
from scripts.database_connection import DatabaseConnection
from scripts.bronze_loader import BronzeLoader
from scripts.managers.schema_manager import SchemaManager
from scripts.managers.audit_manager import AuditManager
from scripts.bronze_loader import Layer

# database connection
connection = DatabaseConnection(
    POSTGRES_URL,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)
conn = connection.get_connection()

# schema
schema = SchemaManager(conn)
audit = AuditManager(conn)

def extract() -> list[str]:
    print("\n")
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
    print('\n[INFO] Extract successfully ... \n')
    return downloaded_files

def load_to_bronze():
    # L1 --> BRONZE LAYER
    loader = BronzeLoader(conn)
    start = datetime.now()
    
    try:
        schema.execute(Path('db/init/01_schema.sql'))
        schema.execute(Path('db/init/02_bronze_load.sql'))
        schema.execute(Path('db/init/06_audit.sql'))
        loader.load_data(Path("data/raw/raw_yellow_tripdata_2026_01.parquet"), "raw_taxi_trips", Layer.BRONZE)
        loader.load_data(Path("data/raw/taxi_zone_lookup.csv"), "raw_taxi_lookup", Layer.BRONZE)
        
        rows = schema.fetch("""
            SELECT COUNT(*)
            FROM bronze.raw_taxi_trips
        """)
        
        audit.log_pipeline(
            layer="bronze",
            process_name="load to bronze",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=rows,
            status="SUCCESS",
            message="[BRONZE] Bronze layer loaded successfully."
        )
        
        print('\n[INFO] Ingest to Bronze successfully ... \n')
        
    except Exception as e:
        conn.rollback()
        audit.log_pipeline(
            layer="bronze",
            process_name="load to bronze",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=0,
            status="FAILED",
            message=f"[ERROR] {str(e)}"
        )
        raise
 
def transform_to_silver():
    # L2 --> SILVER LAYER
    start = datetime.now()
    try:
        silver_layer = [
            Path('db/init/03_silver_transform.sql'),
            *sorted(Path('db/schemas/silver').glob('*.sql'))
        ]
        schema.execute_many(silver_layer)
        
        rows_taxi_cleaned = schema.fetch("""
        SELECT COUNT(*) 
        FROM silver.taxi_trips_cleaned
        """)
        
        rows_data_quality_issues = schema.fetch("""
        SELECT COUNT(*) 
        FROM silver.data_quality_issues
        """)
        
        print(f'[LOAD TO SILVER] Loaded {rows_taxi_cleaned:,} valid rows ...')
        print(f'[LOAD TO SILVER] Loaded {rows_data_quality_issues:,} invalid rows ...')
         
        audit.log_pipeline(
            layer="silver",
            process_name="load valid data to silver",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=rows_taxi_cleaned,
            status="SUCCESS",
            message="[SILVER] Valid data loaded successfully."
        )
        
        audit.log_pipeline(
            layer="silver",
            process_name="load invalid data to silver",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=rows_data_quality_issues,
            status="SUCCESS",
            message="[SILVER] Invalid Data loaded successfully."
        )
        
        print('\n[INFO] Transform to Silver successfully ... \n')
        
    except Exception as e:
        conn.rollback()
        audit.log_pipeline(
            layer="silver",
            process_name="silver transform",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=0,
            status="FAILED",
            message=f"[ERROR] {str(e)}"
        )
        raise

def analytics_to_gold():
    # L3 --> GOLD LAYER
    start = datetime.now()
    
    try:
        gold_layer = [
            Path('db/init/04_gold_mart.sql'),
            *sorted(Path('db/schemas/gold').glob('*.sql'))
        ]
        schema.execute_many(gold_layer)
        
        audit.log_pipeline(
            layer="gold",
            process_name="load to gold mart",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=None,
            status="SUCCESS",
            message="[GOLD] Silver layer loaded successfully."
        )
        print('\n[INFO] Analytics to Gold successfully ... \n')
        
    except Exception as e:
        conn.rollback()
        audit.log_pipeline(
            layer="gold",
            process_name="load to gold mart",
            start_time=start,
            end_time=datetime.now(),
            rows_processed=0,
            status="FAILED",
            message=f"[ERROR] {str(e)}"
        )
        raise

def create_views():
    # CREATE VIEWS
    schema.execute(Path('db/init/05_views.sql'))
    print('\n[INFO] Views created successfully ... \n')

if __name__ == '__main__':
    extract()
    load_to_bronze()
    transform_to_silver()
    analytics_to_gold()
    create_views()