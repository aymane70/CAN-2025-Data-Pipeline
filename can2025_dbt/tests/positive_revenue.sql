-- Test: All revenue values should be positive
SELECT *
FROM {{ ref('stg_ticket_sales') }}
WHERE total_revenue < 0
   OR price_usd < 0
   OR quantity < 0
