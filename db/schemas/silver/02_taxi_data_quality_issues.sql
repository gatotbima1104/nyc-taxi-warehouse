BEGIN;

TRUNCATE TABLE silver.data_quality_issues RESTART IDENTITY;

INSERT INTO silver.data_quality_issues (
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    pickup_location_id,
    dropoff_location_id,
    error_type
)
SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    PULocationID,
    DOLocationID,
    CASE
        WHEN tpep_pickup_datetime >= tpep_dropoff_datetime THEN 'duration invalid'
        WHEN trip_distance <= 0 THEN 'distance invalid'
        WHEN passenger_count <= 0 THEN 'passenger invalid'
        WHEN fare_amount <= 0 THEN 'fare_amount invalid'
        WHEN tip_amount <= 0 THEN 'tip_amount invalid'
    END
FROM bronze.raw_taxi_trips
WHERE tpep_pickup_datetime >= tpep_dropoff_datetime 
    OR trip_distance <= 0
    OR passenger_count <= 0
    OR fare_amount <= 0
    OR tip_amount < 0;

COMMIT;