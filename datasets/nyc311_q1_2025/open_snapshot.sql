CREATE OR REPLACE VIEW nyc_311_requests AS
SELECT *
FROM read_parquet(
  '.interview-work/nyc311-q1-2025/nyc_311_requests_2025_q1.parquet'
);

CREATE OR REPLACE VIEW nyc_311_events AS
SELECT *
FROM read_parquet(
  '.interview-work/nyc311-q1-2025/nyc_311_events_2025_q1.parquet'
);

SELECT
  (SELECT count(*) FROM nyc_311_requests) AS request_rows,
  (SELECT count(*) FROM nyc_311_events) AS event_rows;

