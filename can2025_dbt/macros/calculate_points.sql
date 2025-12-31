{% macro calculate_points(home_score, away_score, is_home_team) %}
    {% if is_home_team %}
        CASE 
            WHEN {{ home_score }} > {{ away_score }} THEN 3
            WHEN {{ home_score }} = {{ away_score }} THEN 1
            ELSE 0
        END
    {% else %}
        CASE 
            WHEN {{ away_score }} > {{ home_score }} THEN 3
            WHEN {{ away_score }} = {{ home_score }} THEN 1
            ELSE 0
        END
    {% endif %}
{% endmacro %}
