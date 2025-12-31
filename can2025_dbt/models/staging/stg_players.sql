{{ config(materialized='view') }}

SELECT
    player_id,
    team_id,
    TRIM(player_name) as player_name,
    position,
    age,
    CASE 
        WHEN age < 23 THEN 'Youth'
        WHEN age BETWEEN 23 AND 28 THEN 'Prime'
        WHEN age BETWEEN 29 AND 32 THEN 'Experienced'
        ELSE 'Veteran'
    END as age_category,
    height_cm,
    club,
    market_value_millions,
    CASE 
        WHEN market_value_millions < 5 THEN 'Low'
        WHEN market_value_millions BETWEEN 5 AND 20 THEN 'Medium'
        ELSE 'High'
    END as market_value_tier
FROM {{ source('can2025_raw', 'players') }}
