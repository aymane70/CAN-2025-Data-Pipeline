{{ config(materialized='view') }}

WITH home_matches AS (
    SELECT
        home_team_id as team_id,
        match_id,
        home_score as goals_scored,
        away_score as goals_conceded,
        home_score - away_score as goal_difference,
        CASE 
            WHEN home_score > away_score THEN 3
            WHEN home_score = away_score THEN 1
            ELSE 0
        END as points,
        CASE WHEN away_score = 0 THEN 1 ELSE 0 END as clean_sheet,
        CASE 
            WHEN home_score > away_score THEN 'Win'
            WHEN home_score = away_score THEN 'Draw'
            ELSE 'Loss'
        END as outcome
    FROM {{ ref('stg_matches') }}
),
away_matches AS (
    SELECT
        away_team_id as team_id,
        match_id,
        away_score as goals_scored,
        home_score as goals_conceded,
        away_score - home_score as goal_difference,
        CASE 
            WHEN away_score > home_score THEN 3
            WHEN away_score = home_score THEN 1
            ELSE 0
        END as points,
        CASE WHEN home_score = 0 THEN 1 ELSE 0 END as clean_sheet,
        CASE 
            WHEN away_score > home_score THEN 'Win'
            WHEN away_score = home_score THEN 'Draw'
            ELSE 'Loss'
        END as outcome
    FROM {{ ref('stg_matches') }}
)
SELECT * FROM home_matches
UNION ALL
SELECT * FROM away_matches
