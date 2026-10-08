with source as (

    select * from {{ source('raw_data', 'accounts') }}

),

cleaned as (

    select
        account_id,
        customer_id,
        account_type,
        currency,
        opened_date,
        is_active
    from source

)

select * from cleaned
