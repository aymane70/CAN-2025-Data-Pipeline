{{ config(materialized='view') }}

SELECT
    stadium_id,
    TRIM(stadium_name) as stadium_name,
    TRIM(city) as city,
    capacity
FROM {{ source('can2025_raw', 'stadiums') }}
