# Neobank Data Pipeline

An end-to-end ELT pipeline built on AWS using **synthetic** neobank data (customers, accounts, transactions).

> All data in this repository is randomly generated. It contains no real customer data and is not derived from any employer's systems.

## Architecture

```
Raw CSV files
   -> Amazon S3 (data lake)
   -> Amazon Redshift Serverless (warehouse)
   -> dbt (transformations)
```

| Layer | Tool | Purpose |
|---|---|---|
| Landing zone | Amazon S3 | Stores raw CSV files |
| Warehouse | Amazon Redshift Serverless | Holds raw tables loaded with `COPY` |
| Transformation | dbt Core | Staging -> intermediate -> mart models, with data-quality tests |

## Dataset

Generated with `generate_data.py` (fixed random seed, so output is reproducible):

- `customers` — 500 rows
- `accounts` — ~760 rows, each linked to a customer
- `transactions` — ~33,000 rows, each linked to an account, spanning 12 months

## Project status

- [x] Synthetic data generator
- [x] S3 bucket and raw file upload
- [x] Redshift Serverless setup
- [x] Raw tables loaded with `COPY`
- [ ] dbt project: staging models
- [ ] dbt project: mart model (monthly transaction summary per customer segment)
- [ ] dbt tests (unique, not_null, relationships)
- [ ] Architecture diagram and sample output

## How to reproduce

_To be completed as the project progresses._

### 1. Generate the data

```bash
python3 -m venv venv
source venv/bin/activate
pip install faker
python generate_data.py
```

This creates three CSV files in a local `data/` folder.

## What I learned

_To be completed at the end of the project._

## Design notes

- **Regions:** the S3 data lake is in `eu-central-1` and Redshift Serverless is in `us-east-1`. `COPY` uses the `REGION` option to load across regions. With real EU customer data I would keep both in one EU region for data residency and to avoid cross-region transfer costs.
- **Schema name:** the raw schema is called `raw_data` because `raw` is a reserved word in Redshift.
- **Currencies:** transactions are in EUR, USD and GBP, so aggregates group by currency instead of summing amounts across currencies.
