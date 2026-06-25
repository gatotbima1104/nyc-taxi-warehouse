import pyarrow.parquet as pq
import pyarrow.csv as pc
from pathlib import Path

table = pq.read_table(Path("data/raw/raw_yellow_tripdata_2026_01.parquet"))
print(table.schema)

table = pc.read_csv("../data/raw/taxi_zone_lookup.csv")
print(table.schema)
