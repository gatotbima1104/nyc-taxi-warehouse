from etl.extract import TaxiExtractor
from etl.transform import TaxiTransformer
from utils.constants import TAXI_JAN_2026_FILE, TAXI_JAN_2026_URL, TAXI_ZONE_LOOKUP_TABLE, TAXI_ZONE_LOOKUP_URL, TRANFORMED_FILE

# Extract
extract_files = [
    (TAXI_JAN_2026_URL, TAXI_JAN_2026_FILE),
    (TAXI_ZONE_LOOKUP_URL, TAXI_ZONE_LOOKUP_TABLE)
]

print("\n=========================== Extracting Data ....\n")
extractor = TaxiExtractor()
downloaded_files = []

for url, filename in extract_files:
    downloaded_files.append(
        extractor.extract(url, filename)
    )
print("=========================== Completed .....\n")

# Transform
transformer = TaxiTransformer()
taxi_transformer = transformer.transform(
    filepath=downloaded_files[0],
    filepath_lookup_table=downloaded_files[1],
    output_name=TRANFORMED_FILE
)