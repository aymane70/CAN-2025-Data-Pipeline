{{ config(materialized='view') }}

SELECT
    team_id,
    TRIM(team_name) as team_name,
    UPPER(group_name) as group_name,
    fifa_ranking,
    TRIM(coach_name) as coach_name,
    coach_nationality
FROM {{ source('can2025_raw', 'teams') }}
