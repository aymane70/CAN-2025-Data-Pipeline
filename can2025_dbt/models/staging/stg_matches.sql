{{ config(materialized='view') }}

SELECT
    match_id,
    match_date,
    stadium_id,
    home_team_id,
    away_team_id,
    home_score,
    away_score,
    home_score + away_score as total_goals,
    home_score - away_score as goal_difference,
    CASE 
        WHEN home_score > away_score THEN 'Home Win'
        WHEN home_score < away_score THEN 'Away Win'
        ELSE 'Draw'
    END as match_result,
    attendance,
    round,
    CASE 
        WHEN round LIKE 'Group%' THEN 'Group Stage'
        WHEN round = 'Round of 16' THEN 'Round of 16'
        WHEN round = 'Quarter-finals' THEN 'Quarter Finals'
        WHEN round = 'Semi-finals' THEN 'Semi Finals'
        ELSE 'Final'
    END as tournament_phase,
    status
FROM {{ source('can2025_raw', 'matches') }}
