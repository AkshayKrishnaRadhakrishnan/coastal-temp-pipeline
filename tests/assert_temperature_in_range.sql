select *
from {{ ref('stg_hourly_temperature') }}
where temperature_c < {{ var('min_valid_temp_c') }}
   or temperature_c > {{ var('max_valid_temp_c') }}