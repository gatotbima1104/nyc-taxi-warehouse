from etl.extract import TaxiExtractor
from etl.transform import TaxiTransformer
from etl.load import TaxiLoader
from utils.constants import TAXI_JAN_2026_FILE, TAXI_JAN_2026_URL, TAXI_ZONE_LOOKUP_TABLE, TAXI_ZONE_LOOKUP_URL, TRANFORMED_FILE, VALID_DATA_PATH, INVALID_DATA_PATH

# Extract
print("\n=========================== Extracting Data ....\n")
extract_files = [
    (TAXI_JAN_2026_URL, TAXI_JAN_2026_FILE),
    (TAXI_ZONE_LOOKUP_URL, TAXI_ZONE_LOOKUP_TABLE)
]


extractor = TaxiExtractor()
downloaded_files = []

for url, filename in extract_files:
    downloaded_files.append(
        extractor.extract(url, filename)
    )
print("============================= Completed ....\n")

# Transform
print("\n=========================== Transorming Data ....\n")
transformer = TaxiTransformer()
taxi_transformer = transformer.transform(
    filepath=downloaded_files[0],
    filepath_lookup_table=downloaded_files[1],
    output_name=TRANFORMED_FILE
)
print("\n============================= Completed ....\n")

# Load
print("\n=========================== Loading Data ....\n")
loader = TaxiLoader()
valid_data, invalid_data = loader.validate_data(
    dataframe=taxi_transformer
)

load_files = {
    VALID_DATA_PATH : valid_data,
    INVALID_DATA_PATH : invalid_data
}

for path, dataframe in load_files.items():
    loader.load(
        dataframe=dataframe,
        output_path=path
    )
print("\n============================= Completed ....\n")