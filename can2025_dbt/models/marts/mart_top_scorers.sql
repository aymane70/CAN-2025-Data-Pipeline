{{ config(materialized='table') }}

SELECT
    p.player_id,
    p.player_name,
    t.team_name,
    p.position,
    p.age,
    p.age_category,
    ps.total_goals,
    ps.matches_with_events,
    ROUND(ps.total_goals / NULLIF(ps.matches_with_events, 0), 2) as goals_per_match,
    ps.avg_goal_minute,
    RANK() OVER (ORDER BY ps.total_goals DESC) as scorer_rank
FROM {{ ref('stg_players') }} p
JOIN {{ ref('int_player_statistics') }} ps ON p.player_id = ps.player_id
JOIN {{ ref('stg_teams') }} t ON p.team_id = t.team_id
WHERE ps.total_goals > 0
ORDER BY ps.total_goals DESC
