{{ config(materialized='view') }}

SELECT
    sale_id,
    match_id,
    sale_date,
    ticket_category,
    quantity,
    price_usd,
    total_revenue,
    CASE ticket_category
        WHEN 'VIP' THEN 1
        WHEN 'Premium' THEN 2
        WHEN 'Standard' THEN 3
        WHEN 'Economy' THEN 4
    END as category_rank
FROM {{ source('can2025_raw', 'ticket_sales') }}
