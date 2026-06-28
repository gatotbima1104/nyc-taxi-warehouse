BEGIN;

TRUNCATE TABLE silver.taxi_zones CASCADE;

INSERT INTO silver.taxi_zones (
    location_id,
    borough,
    zone,
    service_zone
)
SELECT
    LocationID,
    COALESCE(Borough, 'Unknown') as borough,
    COALESCE(Zone, 'Unknown') as zone,
    COALESCE(service_zone, 'Unknown') as service_zone
FROM bronze.raw_taxi_lookup;

COMMIT;