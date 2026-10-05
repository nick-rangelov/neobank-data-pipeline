# -*- coding: utf-8 -*-
"""
Generates a small, realistic synthetic banking dataset:
- customers.csv   : customer master data
- accounts.csv     : one or more accounts per customer
- transactions.csv : transactions against those accounts, spanning 12 months

Designed to mirror a simplified neobank data model (customers -> accounts -> transactions),
loaded raw into Redshift, then transformed with dbt into staging/intermediate/mart layers.
"""
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUT_DIR = "data"
import os
os.makedirs(OUT_DIR, exist_ok=True)

N_CUSTOMERS = 500
ACCOUNT_TYPES = ["checking", "savings", "business"]
CURRENCIES = ["EUR", "USD", "GBP"]
SEGMENTS = ["retail", "premium", "business"]
COUNTRIES = ["Netherlands", "Germany", "France", "Belgium", "Italy", "Spain", "Austria"]
TXN_TYPES = ["card_payment", "transfer_in", "transfer_out", "atm_withdrawal", "direct_debit", "deposit"]
MERCHANT_CATEGORIES = ["groceries", "dining", "travel", "utilities", "entertainment", "transport",
                        "shopping", "subscriptions", "salary", "rent"]

start_date = datetime(2025, 10, 1)
end_date = datetime(2026, 9, 30)

# ---------------- customers.csv ----------------
customers = []
for cust_id in range(1, N_CUSTOMERS + 1):
    signup_date = fake.date_between(start_date=start_date - timedelta(days=700), end_date=end_date)
    customers.append({
        "customer_id": cust_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "country": random.choice(COUNTRIES),
        "segment": random.choices(SEGMENTS, weights=[70, 20, 10])[0],
        "signup_date": signup_date.isoformat(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
    })

with open(f"{OUT_DIR}/customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
    writer.writeheader()
    writer.writerows(customers)

# ---------------- accounts.csv ----------------
accounts = []
account_id = 1
customer_accounts = {}  # customer_id -> list of account_ids
for cust in customers:
    n_accounts = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
    customer_accounts[cust["customer_id"]] = []
    for _ in range(n_accounts):
        acct_type = "business" if cust["segment"] == "business" else random.choice(["checking", "savings"])
        opened = fake.date_between(start_date=datetime.strptime(cust["signup_date"], "%Y-%m-%d"),
                                    end_date=end_date)
        accounts.append({
            "account_id": account_id,
            "customer_id": cust["customer_id"],
            "account_type": acct_type,
            "currency": random.choices(CURRENCIES, weights=[75, 15, 10])[0],
            "opened_date": opened.isoformat(),
            "is_active": random.choices([True, False], weights=[92, 8])[0],
        })
        customer_accounts[cust["customer_id"]].append(account_id)
        account_id += 1

with open(f"{OUT_DIR}/accounts.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(accounts[0].keys()))
    writer.writeheader()
    writer.writerows(accounts)

# ---------------- transactions.csv ----------------
transactions = []
txn_id = 1
all_account_ids = [a["account_id"] for a in accounts]
account_lookup = {a["account_id"]: a for a in accounts}

for acct in accounts:
    opened = datetime.strptime(acct["opened_date"], "%Y-%m-%d")
    txn_start = max(opened, start_date)
    if txn_start > end_date:
        continue
    n_txns = random.randint(5, 80)
    for _ in range(n_txns):
        days_range = (end_date - txn_start).days
        if days_range <= 0:
            continue
        txn_date = txn_start + timedelta(days=random.randint(0, days_range))
        txn_type = random.choice(TXN_TYPES)
        if txn_type in ("transfer_in", "deposit"):
            amount = round(random.uniform(10, 3000), 2)
        elif txn_type == "atm_withdrawal":
            amount = -round(random.uniform(20, 300), 2)
        else:
            amount = -round(random.uniform(2, 500), 2)

        transactions.append({
            "transaction_id": txn_id,
            "account_id": acct["account_id"],
            "transaction_date": txn_date.strftime("%Y-%m-%d"),
            "transaction_type": txn_type,
            "merchant_category": random.choice(MERCHANT_CATEGORIES) if amount < 0 else "",
            "amount": amount,
            "currency": acct["currency"],
        })
        txn_id += 1

with open(f"{OUT_DIR}/transactions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(transactions[0].keys()))
    writer.writeheader()
    writer.writerows(transactions)

print(f"customers:    {len(customers)} rows")
print(f"accounts:     {len(accounts)} rows")
print(f"transactions: {len(transactions)} rows")
