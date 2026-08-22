import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MySQL
connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

# SQL query
query = "SELECT * FROM orders"

# Read SQL data into Pandas
df = pd.read_sql(query, connection)

products_query = "SELECT * FROM products"

products_df = pd.read_sql(products_query, connection)

# Close database connection
connection.close()

# Display first 5 rows
print(df.head())

# Dataset information
print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

# Business KPIs
total_revenue = df["sales"].sum()
total_profit = df["profit"].sum()
total_orders = df["order_id"].count()
average_order_value = total_revenue / total_orders

print("\nTotal Revenue:")
print(total_revenue)

print("\nTotal Profit:")
print(total_profit)

print("\nTotal Orders:")
print(total_orders)

print("\nAverage Order Value:")
print(average_order_value)

df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.month

monthly_revenue = (
    df.groupby("month")["sales"]
    .sum()
    .reset_index()
    .rename(columns={"sales": "revenue"})
    
)
monthly_revenue["revenue_change"] = monthly_revenue["revenue"].pct_change() * 100
monthly_revenue["revenue"] = monthly_revenue["revenue"].round(2)
monthly_revenue["revenue_change"] = monthly_revenue["revenue_change"].round(2)

print("\nMonthly Revenue:")
print(monthly_revenue)

orders_with_products = df.merge(
    products_df,
    on="product_id",
    how="left"
)

print(orders_with_products.head())


category_revenue = (
    orders_with_products
    .groupby("category")["sales"]
    .sum()
    .reset_index()
    .rename(columns={"sales": "revenue"})
    .sort_values("revenue", ascending=False)
)

print("\nRevenue by Category:")
print(category_revenue)