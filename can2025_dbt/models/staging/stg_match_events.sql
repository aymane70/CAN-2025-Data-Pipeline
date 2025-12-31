{{ config(materialized='view') }}

SELECT
    event_id,
    match_id,
    player_id,
    event_type,
    minute,
    CASE 
        WHEN minute <= 45 THEN 'First Half'
        ELSE 'Second Half'
    END as match_period,
    team_id,
    CASE WHEN event_type = 'Goal' THEN 1 ELSE 0 END as is_goal,
    CASE WHEN event_type IN ('Yellow Card', 'Red Card') THEN 1 ELSE 0 END as is_card
FROM {{ source('can2025_raw', 'match_events') }}
