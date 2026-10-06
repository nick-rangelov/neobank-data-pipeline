-- Raw layer: create schema and tables, then load from S3.
-- Replace <YOUR_BUCKET> with your S3 bucket and <BUCKET_REGION> with its region.
-- "raw" is a reserved word in Redshift, so the schema is called raw_data.

create schema if not exists raw_data;

create table raw_data.customers (
    customer_id   integer,
    first_name    varchar(100),
    last_name     varchar(100),
    email         varchar(255),
    country       varchar(100),
    segment       varchar(50),
    signup_date   date,
    date_of_birth date
);

create table raw_data.accounts (
    account_id    integer,
    customer_id   integer,
    account_type  varchar(50),
    currency      varchar(10),
    opened_date   date,
    is_active     boolean
);

create table raw_data.transactions (
    transaction_id    integer,
    account_id        integer,
    transaction_date  date,
    transaction_type  varchar(50),
    merchant_category varchar(100),
    amount            decimal(12,2),
    currency          varchar(10)
);

copy raw_data.customers    from 's3://<YOUR_BUCKET>/raw/customers/'
    iam_role default region '<BUCKET_REGION>' csv ignoreheader 1 emptyasnull;
copy raw_data.accounts     from 's3://<YOUR_BUCKET>/raw/accounts/'
    iam_role default region '<BUCKET_REGION>' csv ignoreheader 1 emptyasnull;
copy raw_data.transactions from 's3://<YOUR_BUCKET>/raw/transactions/'
    iam_role default region '<BUCKET_REGION>' csv ignoreheader 1 emptyasnull;
