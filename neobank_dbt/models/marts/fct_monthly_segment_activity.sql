with transactions as (

    select * from {{ ref('stg_transactions') }}

),

accounts as (

    select * from {{ ref('stg_accounts') }}

),

customers as (

    select * from {{ ref('stg_customers') }}

),

joined as (

    select
        date_trunc('month', t.transaction_date)::date as activity_month,
        c.segment,
        t.currency,
        t.transaction_id,
        t.amount,
        t.direction,
        a.customer_id
    from transactions t
    join accounts a on t.account_id = a.account_id
    join customers c on a.customer_id = c.customer_id

),

monthly as (

    select
        activity_month,
        segment,
        currency,
        count(*)                                                as transaction_count,
        count(distinct customer_id)                             as active_customers,
        sum(case when direction = 'credit' then amount else 0 end) as total_credits,
        sum(case when direction = 'debit'  then amount else 0 end) as total_debits,
        sum(amount)                                             as net_amount,
        round(avg(abs(amount)), 2)                              as avg_transaction_size
    from joined
    group by 1, 2, 3

)

select * from monthly
