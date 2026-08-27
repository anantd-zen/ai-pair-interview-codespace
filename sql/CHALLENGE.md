# SQL challenge: customer revenue by region

Complete the query in `sql/challenge.sql`. Produce one row for every customer,
including customers with no completed orders.

Return these columns in this exact order:

1. `region`
2. `customer_id`
3. `customer_name`
4. `completed_order_count`
5. `completed_revenue_cents`
6. `latest_completed_at`
7. `revenue_rank_in_region`

Only `completed` orders contribute. Customers without completed orders have
zero count and revenue and a null latest timestamp. Rank within each region by
revenue descending, breaking ties by `customer_id` ascending. Sort by region,
then rank.

```bash
python scripts/run_sql_challenge.py
pytest -m sql_challenge
```

