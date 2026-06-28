DROP TABLE IF EXISTS silver.data_quality_issues;
DROP TABLE IF EXISTS silver.taxi_trips_cleaned;
DROP TABLE IF EXISTS silver.taxi_zones;

CREATE TABLE silver.taxi_zones(
    location_id INTEGER PRIMARY KEY,
    borough TEXT NOT NULL,
    zone TEXT NOT NULL,
    service_zone TEXT NOT NULL
);

CREATE TABLE silver.taxi_trips_cleaned (
    trip_id BIGSERIAL PRIMARY KEY,
    vendor_id INTEGER NOT NULL,

    pickup_datetime TIMESTAMP NOT NULL,
    pickup_date DATE NOT NULL,
    pickup_hour INTEGER NOT NULL,
    pickup_day_time TEXT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    time_period TEXT NOT NULL,
    pickup_borough TEXT NOT NULL,
    pickup_zone TEXT NOT NULL,

    dropoff_datetime TIMESTAMP NOT NULL,
    dropoff_borough TEXT NOT NULL,
    dropoff_zone TEXT NOT NULL,

    passenger_count INTEGER NOT NULL,

    trip_distance NUMERIC(10,2) NOT NULL,
    trip_duration_minutes NUMERIC(10,2) NOT NULL,

    rate_code_id INTEGER NOT NULL,
    store_and_fwd_flag TEXT NOT NULL,   
    pickup_location_id INTEGER NOT NULL,
    dropoff_location_id INTEGER NOT NULL,
    payment_type TEXT NOT NULL,
    fare_amount NUMERIC(10,2) NOT NULL,
    -- extra NUMERIC(10,2) NOT NULL,
    -- mta_tax NUMERIC(10,2) NOT NULL,
    tip_amount NUMERIC(10,2) NOT NULL,
    -- tolls_amount NUMERIC(10,2),
    -- improvement_surcharge NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    -- congestion_surcharge NUMERIC(10,2),
    -- airport_fee NUMERIC(10,2),   
    -- cbd_congestion_fee NUMERIC(10,2),

    CONSTRAINT fk_pickup
        FOREIGN KEY(pickup_location_id) 
        REFERENCES silver.taxi_zones(location_id),

    CONSTRAINT fk_dropoff
        FOREIGN KEY(dropoff_location_id) 
        REFERENCES silver.taxi_zones(location_id)
);

CREATE TABLE silver.data_quality_issues (
    issue_id BIGSERIAL PRIMARY KEY,
    vendor_id INTEGER,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    error_type TEXT NOT NULL
);