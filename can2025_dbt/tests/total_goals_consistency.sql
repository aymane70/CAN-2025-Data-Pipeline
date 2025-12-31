-- Test: Total goals in match_events should match sum of home_score + away_score in matches
WITH match_goals AS (
    SELECT 
        m.match_id,
        m.home_score + m.away_score as expected_goals,
        COUNT(CASE WHEN e.event_type = 'Goal' THEN 1 END) as actual_goals
    FROM {{ ref('stg_matches') }} m
    LEFT JOIN {{ ref('stg_match_events') }} e 
        ON m.match_id = e.match_id 
        AND e.event_type = 'Goal'
    GROUP BY m.match_id, m.home_score, m.away_score
)
SELECT *
FROM match_goals
WHERE expected_goals != actual_goals
