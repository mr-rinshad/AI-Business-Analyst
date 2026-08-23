DATABASE_SCHEMA = """
Database: ai_business_analyst

Table: orders
Columns:
- order_id
- customer_id
- product_id
- order_date
- quantity
- unit_price
- discount
- sales
- cost
- profit

Table: products
Columns:
- product_id
- product_name
- category
- unit_price

Table: customers
Columns:
- customer_id
- customer_name
- region
- email
"""