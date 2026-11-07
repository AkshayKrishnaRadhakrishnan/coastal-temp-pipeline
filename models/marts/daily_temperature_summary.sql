select
    location,
    cast(observed_at as date) as reading_date,
    min(temperature_c) as min_temp_c,
    max(temperature_c) as max_temp_c,
    round(avg(temperature_c), 1) as avg_temp_c,
    count(*) as readings,
    max(temperature_c) > {{ var('high_temp_threshold_c') }} as high_temp_alert,
    min(temperature_c) < {{ var('low_temp_threshold_c') }} as low_temp_alert
from {{ ref('stg_hourly_temperature') }}
group by location, cast(observed_at as date)