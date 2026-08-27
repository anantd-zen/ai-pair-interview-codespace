# Example SQL prompt: customer revenue by region

Complete `sql/challenge.sql`. Produce one row for every customer, including
customers with no completed orders.

Return these columns in this exact order:

1. `region`
2. `customer_id`
3. `customer_name`
4. `completed_order_count`
5. `completed_revenue_cents`
6. `latest_completed_at`
7. `revenue_rank_in_region`

Only `completed` orders contribute. Rank within each region by completed
revenue descending, breaking ties by `customer_id` ascending.

```bash
uv run python run_query.py
uv run pytest
```

