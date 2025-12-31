{{ config(materialized='view') }}

SELECT
    player_id,
    COUNT(CASE WHEN event_type = 'Goal' THEN 1 END) as total_goals,
    COUNT(CASE WHEN event_type = 'Yellow Card' THEN 1 END) as yellow_cards,
    COUNT(CASE WHEN event_type = 'Red Card' THEN 1 END) as red_cards,
    COUNT(DISTINCT match_id) as matches_with_events,
    AVG(CASE WHEN event_type = 'Goal' THEN minute END) as avg_goal_minute
FROM {{ ref('stg_match_events') }}
GROUP BY player_id
