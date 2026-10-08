with source as (

    select * from {{ source('raw_data', 'transactions') }}

),

cleaned as (

    select
        transaction_id,
        account_id,
        transaction_date,
        transaction_type,
        merchant_category,
        amount,
        currency,
        case when amount >= 0 then 'credit' else 'debit' end as direction
    from source

)

select * from cleaned
