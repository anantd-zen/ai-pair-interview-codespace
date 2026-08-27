CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR NOT NULL,
    region VARCHAR NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    ordered_at TIMESTAMP NOT NULL,
    status VARCHAR NOT NULL,
    total_cents INTEGER NOT NULL
);

