CREATE EXTERNAL TABLE IF NOT EXISTS bd_events.fact_purchase (
    event_id STRING,
    user_id STRING,
    event_timestamp TIMESTAMP,
    amount FLOAT64,
    currency STRING,
    device STRING,
    country STRING
)
OPTIONS (
    format='CSV',
    field_delimiter=',',
    skip_leading_rows=1,
    uris =['gs://desafio_bucket/silver_layer/purchase_folder/*.csv']
)