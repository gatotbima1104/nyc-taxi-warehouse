from etl.extract import TaxiExtractor
from etl.transform import TaxiTransformer
from etl.load import TaxiLoader
from utils.helpers import Helper
from utils.constants import TAXI_JAN_2026_FILE, TAXI_JAN_2026_URL, TAXI_ZONE_LOOKUP_TABLE, TAXI_ZONE_LOOKUP_URL, TRANFORMED_FILE, VALID_DATA_PATH, INVALID_DATA_PATH

# Extract
Helper.log("Extracting Data ...")
extract_files = [
    (TAXI_JAN_2026_URL, TAXI_JAN_2026_FILE),
    (TAXI_ZONE_LOOKUP_URL, TAXI_ZONE_LOOKUP_TABLE)
]

extractor = TaxiExtractor()
downloaded_files = []

for url, filename in extract_files:
    downloaded_files.append(extractor.extract(url, filename))
Helper.log("Completed")

# Transform
Helper.log("Transforming Data  ...")
transformer = TaxiTransformer()
taxi_transformer = transformer.transform(
    filepath=downloaded_files[0],
    filepath_lookup_table=downloaded_files[1],
    output_name=TRANFORMED_FILE
)
Helper.log("Completed")

# Load
loader = TaxiLoader()

Helper.log("Validating Data  ...")
valid_data, invalid_data = loader.validate_data(dataframe=taxi_transformer)
Helper.log("Completed")

load_files = {
    VALID_DATA_PATH : valid_data,
    INVALID_DATA_PATH : invalid_data
}

Helper.log("Loading Data  ...")
for path, dataframe in load_files.items():
    loader.load(dataframe=dataframe, output_path=path)
Helper.log("Completed")