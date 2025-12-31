{{ config(materialized='table') }}

SELECT
    t.team_id,
    t.team_name,
    t.group_name,
    COUNT(tp.match_id) as matches_played,
    SUM(CASE WHEN tp.outcome = 'Win' THEN 1 ELSE 0 END) as wins,
    SUM(CASE WHEN tp.outcome = 'Draw' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN tp.outcome = 'Loss' THEN 1 ELSE 0 END) as losses,
    SUM(tp.goals_scored) as goals_for,
    SUM(tp.goals_conceded) as goals_against,
    SUM(tp.goal_difference) as goal_difference,
    SUM(tp.points) as points,
    ROUND(SUM(tp.points) / COUNT(tp.match_id), 2) as points_per_game,
    RANK() OVER (PARTITION BY t.group_name ORDER BY SUM(tp.points) DESC, SUM(tp.goal_difference) DESC) as group_position
FROM {{ ref('stg_teams') }} t
LEFT JOIN {{ ref('int_team_performance') }} tp ON t.team_id = tp.team_id
GROUP BY t.team_id, t.team_name, t.group_name
ORDER BY t.group_name, group_position
