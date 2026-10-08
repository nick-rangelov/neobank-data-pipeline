with source as (

    select * from {{ source('raw_data', 'customers') }}

),

cleaned as (

    select
        customer_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as full_name,
        lower(email) as email,
        country,
        segment,
        signup_date,
        date_of_birth
    from source

)

select * from cleaned
