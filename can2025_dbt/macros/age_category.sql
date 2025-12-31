{% macro age_category(age) %}
    CASE 
        WHEN {{ age }} < 23 THEN 'Youth'
        WHEN {{ age }} BETWEEN 23 AND 28 THEN 'Prime'
        WHEN {{ age }} BETWEEN 29 AND 32 THEN 'Experienced'
        ELSE 'Veteran'
    END
{% endmacro %}
