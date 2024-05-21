
WITH cleaned_data AS (
    SELECT
        city,
        city_ascii,
        lat,
        lng,
        country,
        iso2,
        iso3,
        admin_name,
        capital,
        population,
        id
    FROM
        {{ ref('cities') }}
    WHERE
        population IS NOT NULL
        AND country != ''
        AND lat IS NOT NULL
        AND lng IS NOT NULL
)

SELECT
    *
FROM
    cleaned_data
