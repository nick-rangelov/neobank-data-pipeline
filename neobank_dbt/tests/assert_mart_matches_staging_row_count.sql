-- Singular test: passes when it returns zero rows.
-- Every staged transaction must appear in the mart exactly once.
select m.mart_total, s.stg_total
from (
    select sum(transaction_count) as mart_total
    from {{ ref('fct_monthly_segment_activity') }}
) m
cross join (
    select count(*) as stg_total
    from {{ ref('stg_transactions') }}
) s
where m.mart_total != s.stg_total
