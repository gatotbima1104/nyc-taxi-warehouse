from etl.extract import TaxiExtractor
from utils.constants import TAXI_JAN_2026_FILE, TAXI_JAN_2026_URL, TAXI_ZONE_LOOKUP_TABLE, TAXI_ZONE_LOOKUP_URL

# Extract
extractor = TaxiExtractor()
taxi_data_extractor = extractor.extract(
    url=TAXI_JAN_2026_URL,
    filename=TAXI_JAN_2026_FILE
)

taxi_lookup_table = extractor.extract(
    url=TAXI_ZONE_LOOKUP_URL,
    filename=TAXI_ZONE_LOOKUP_TABLE
)
