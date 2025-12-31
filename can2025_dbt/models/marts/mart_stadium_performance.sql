{{ config(materialized='table') }}

SELECT
    s.stadium_id,
    s.stadium_name,
    s.city,
    s.capacity,
    COUNT(m.match_id) as matches_hosted,
    SUM(m.attendance) as total_attendance,
    AVG(m.attendance) as avg_attendance,
    ROUND(SUM(m.attendance) / (COUNT(m.match_id) * s.capacity), 2) as occupancy_rate,
    SUM(m.total_goals) as total_goals,
    AVG(m.total_goals) as avg_goals_per_match
FROM {{ ref('stg_stadiums') }} s
LEFT JOIN {{ ref('stg_matches') }} m ON s.stadium_id = m.stadium_id
GROUP BY s.stadium_id, s.stadium_name, s.city, s.capacity
ORDER BY total_attendance DESC
