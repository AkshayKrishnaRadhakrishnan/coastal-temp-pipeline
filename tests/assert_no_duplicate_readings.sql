select
    location,
    observed_at,
    count(*) as copies
from {{ ref('stg_hourly_temperature') }}
group by location, observed_at
having count(*) > 1