{{ config(materialized='table') }}

SELECT
    m.match_date,
    m.tournament_phase,
    m.round,
    ht.team_name AS home_team,
    aw.team_name AS away_team,
    COUNT(DISTINCT m.match_id) AS matches,
    COALESCE(SUM(r.total_revenue), 0) AS total_revenue,
    COALESCE(AVG(r.total_revenue), 0) AS avg_revenue_per_match,
    COALESCE(SUM(r.vip_revenue), 0) AS vip_revenue,
    COALESCE(SUM(r.total_tickets_sold), 0) AS total_tickets_sold,
    ROUND(
        COALESCE(SUM(r.total_revenue), 0) /
        NULLIF(COALESCE(SUM(r.total_tickets_sold), 0), 0),
        2
    ) AS avg_revenue_per_ticket
FROM `artefactpipeline`.`can2025_transformed`.`stg_matches` m
LEFT JOIN `artefactpipeline`.`can2025_transformed`.`stg_teams` ht
    ON m.home_team_id = ht.team_id
LEFT JOIN `artefactpipeline`.`can2025_transformed`.`stg_teams` aw
    ON m.away_team_id = aw.team_id
LEFT JOIN `artefactpipeline`.`can2025_transformed`.`int_revenue_analysis` r
    ON m.match_id = r.match_id
GROUP BY
    m.match_date,
    m.tournament_phase,
    m.round,
    ht.team_name,
    aw.team_name
ORDER BY m.match_date
