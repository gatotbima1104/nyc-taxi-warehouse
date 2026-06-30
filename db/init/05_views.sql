-- View Trip enriched
DROP VIEW IF EXISTS gold.vw_trip_enriched;
CREATE VIEW gold.vw_trip_enriched AS
SELECT
    tt.trip_id,
    tt.vendor_id,

    tt.pickup_datetime,
    tt.pickup_date,
    tt.pickup_hour,
    tt.pickup_day_time,
    tt.is_weekend,
    tt.time_period,

    tt.payment_type,

    tt.trip_distance,
    tt.trip_duration_minutes,
    tt.passenger_count,
    tt.fare_amount,
    tt.tip_amount,
    tt.total_amount,

    pz.location_id as pickup_location_id,
    pz.borough as pickup_borough,
    pz.zone as pickup_zone,
    pz.service_zone as pickup_service_zone,

    dz.location_id as dropoff_location_id,
    dz.borough as dropoff_borough,
    dz.zone as dropoff_zone,
    dz.service_zone as dropoff_service_zone
FROM silver.taxi_trips_cleaned tt
LEFT JOIN silver.taxi_zones pz
 ON tt.pickup_location_id = pz.location_id
LEFT JOIN silver.taxi_zones dz
 ON tt.dropoff_location_id = dz.location_id;

-- View Daily summary
DROP VIEW IF EXISTS gold.vw_daily_trip_summary;
CREATE VIEW gold.vw_daily_trip_summary AS
SELECT
    pickup_date,
    COUNT(*) as total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(trip_duration_minutes), 2) AS avg_duration
FROM gold.vw_trip_enriched
GROUP BY 1;

-- View Zone performance
DROP VIEW IF EXISTS gold.vw_zone_performance;
CREATE VIEW gold.vw_zone_performance AS
WITH pickup_summary AS (
    SELECT
        pickup_zone AS zone,
        pickup_borough AS borough,
        COUNT(*) AS total_pickup_trips,
        ROUND(SUM(total_amount), 2) AS total_revenue,
        ROUND(AVG(fare_amount), 2) AS avg_fare,
        ROUND(AVG(tip_amount), 2) AS avg_tip
    FROM gold.vw_trip_enriched
    GROUP BY 1,2
),
dropoff_summary AS (
    SELECT
        dropoff_zone AS zone,
        COUNT(*) AS total_dropoff_trips
    FROM gold.vw_trip_enriched
    GROUP BY 1
)
SELECT
    ps.borough,
    ps.zone,
    ps.total_pickup_trips,
    COALESCE(ds.total_dropoff_trips, 0) AS total_dropoff_trips,
    ps.avg_fare,
    ps.avg_tip,
    ps.total_revenue
FROM pickup_summary ps
LEFT JOIN dropoff_summary ds
    ON ps.zone = ds.zone
ORDER BY 5 DESC;