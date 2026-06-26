-- 01_create_tables.sql
-- Schema for the e-commerce analysis database (SQLite syntax).
-- Note: load_data.py creates these tables automatically via pandas.to_sql().
-- This file documents the schema for anyone reviewing the project (and is handy
-- if you migrate to Postgres/MySQL for a more "production" looking setup).

CREATE TABLE IF NOT EXISTS customers (
    customer_id        TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_city       TEXT,
    customer_state      TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id              TEXT PRIMARY KEY,
    product_category_name   TEXT,
    product_weight_g        INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    order_id                   TEXT PRIMARY KEY,
    customer_id                TEXT REFERENCES customers(customer_id),
    order_status                TEXT,
    order_purchase_timestamp    TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id        TEXT REFERENCES orders(order_id),
    order_item_id   TEXT,
    product_id      TEXT REFERENCES products(product_id),
    price           REAL,
    freight_value   REAL
);
