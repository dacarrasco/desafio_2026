CREATE EXTERNAL TABLE IF NOT EXISTS bd_events.fact_login (
    event_id STRING,
    user_id STRING,
    event_timestamp TIMESTAMP,
    device STRING,
    country STRING
)
OPTIONS (
    format='CSV',
    field_delimiter=',',
    skip_leading_rows=1,
    uris =['gs://desafio_bucket/silver_layer/login_folder/*.csv']
)