DROP TABLE IF EXISTS audit.logs;
CREATE TABLE IF NOT EXISTS audit.logs (
    run_id BIGSERIAL PRIMARY KEY,
    layer TEXT NOT NULL,
    process_name TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    rows_processed BIGINT,
    status TEXT NOT NULL,
    message TEXT NOT NULL
);