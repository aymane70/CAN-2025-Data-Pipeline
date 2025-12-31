{{ config(materialized='view') }}

SELECT
    match_id,
    SUM(quantity) as total_tickets_sold,
    SUM(total_revenue) as total_revenue,
    AVG(price_usd) as avg_ticket_price,
    SUM(CASE WHEN ticket_category = 'VIP' THEN total_revenue ELSE 0 END) as vip_revenue,
    SUM(CASE WHEN ticket_category = 'Premium' THEN total_revenue ELSE 0 END) as premium_revenue,
    SUM(CASE WHEN ticket_category = 'Standard' THEN total_revenue ELSE 0 END) as standard_revenue,
    SUM(CASE WHEN ticket_category = 'Economy' THEN total_revenue ELSE 0 END) as economy_revenue
FROM {{ ref('stg_ticket_sales') }}
GROUP BY match_id
