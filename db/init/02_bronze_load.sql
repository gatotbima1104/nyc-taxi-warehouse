DROP TABLE IF EXISTS bronze.raw_taxi_trips;
CREATE TABLE bronze.raw_taxi_trips(
    VendorID INTEGER,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count BIGINT,
    trip_distance DOUBLE PRECISION,
    RatecodeID BIGINT,
    store_and_fwd_flag TEXT,
    PULocationID INTEGER,
    DOLocationID INTEGER,
    payment_type BIGINT,
    fare_amount DOUBLE PRECISION,
    extra DOUBLE PRECISION,
    mta_tax DOUBLE PRECISION,
    tip_amount DOUBLE PRECISION,
    tolls_amount DOUBLE PRECISION,
    improvement_surcharge DOUBLE PRECISION,
    total_amount DOUBLE PRECISION,
    congestion_surcharge DOUBLE PRECISION,
    Airport_fee DOUBLE PRECISION,
    cbd_congestion_fee DOUBLE PRECISION
);

DROP TABLE IF EXISTS bronze.raw_taxi_lookup;
CREATE TABLE bronze.raw_taxi_lookup(
    LocationID BIGINT,
    Borough TEXT,
    Zone TEXT,
    service_zone TEXT
);