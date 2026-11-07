with source as (

    select
        location,
        latitude,
        longitude,
        cast(observed_at as timestamp) as observed_at,
        temperature_c,
        loaded_at
    from {{ source('raw', 'hourly_temperature') }}

),

with_reading as (

    select * from source
    where temperature_c is not null

),

deduped as (

    select
        *,
        row_number() over (
            partition by location, observed_at
            order by loaded_at desc
        ) as row_num
    from with_reading

)

select
    location,
    latitude,
    longitude,
    observed_at,
    temperature_c,
    loaded_at
from deduped
where row_num = 1