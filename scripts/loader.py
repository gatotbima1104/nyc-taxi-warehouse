from utils.helpers import Helper
from io import StringIO
from psycopg2.extensions import connection as PGConnection
from pandas import DataFrame
from enum import StrEnum

class Layer(StrEnum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

class BronzeLoader:
    def __init__(self, connection: PGConnection):
        self.connection = connection

    def load_data(self, filepath: str, table_name: str, layer: Layer | None = None):
        df = self._normalize_dtypes(Helper.load_file(filepath))
        buffer = StringIO()

        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        sql = f"""
        COPY bronze.{table_name}
        FROM STDIN
        WITH (FORMAT CSV)
        """
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.copy_expert(sql, buffer)

        self.connection.commit()

        print(
            f"[LOAD TO {'BRONZE' if layer == 'bronze' else 'SILVER' if layer == 'silver' else 'GOLD'}] successfully loaded {len(df):,} rows --> bronze.{table_name}"
        )

    def _normalize_dtypes(self, df: DataFrame):
        PANDAS_NULLABLE_INTS = [
            "VendorID",
            "passenger_count",
            "RatecodeID",
            "PULocationID",
            "DOLocationID",
            "payment_type",
        ]
        for column in PANDAS_NULLABLE_INTS:
            if column in df.columns:
                df[column] = df[column].astype("Int64")
        return df