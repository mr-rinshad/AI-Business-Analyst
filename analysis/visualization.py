import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
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

# Load orders
query = "SELECT * FROM orders"

df = pd.read_sql(query, connection)

# Convert date column
df["order_date"] = pd.to_datetime(df["order_date"])

# Extract month
df["month"] = df["order_date"].dt.month

# Monthly revenue
monthly_revenue = (
    df.groupby("month")["sales"]
    .sum()
    .reset_index()
)

# Create chart
plt.plot(
    monthly_revenue["month"],
    monthly_revenue["sales"],
    marker="o"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks([1, 2, 3])

plt.grid(True)

plt.show()

products_query = "SELECT * FROM products"

products_df = pd.read_sql(
    products_query,
    connection
)

orders_with_products = df.merge(
    products_df,
    on="product_id",
    how="left"
)

category_revenue = (
    orders_with_products
    .groupby("category")["sales"]
    .sum()
    .reset_index()
    .sort_values("sales", ascending=False)
)

plt.bar(
    category_revenue["category"],
    category_revenue["sales"]
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=20)

plt.show()


category_profit = (
    orders_with_products
    .groupby("category")["profit"]
    .sum()
    .reset_index()
    .sort_values("profit", ascending=False)
)

plt.bar(
    category_profit["category"],
    category_profit["profit"]
)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.xticks(rotation=20)

plt.show()

# Load customers
customers_query = "SELECT * FROM customers"

customers_df = pd.read_sql(
    customers_query,
    connection
)

orders_with_customers = df.merge(
    customers_df,
    on="customer_id",
    how="left"
)

customer_revenue = (
    orders_with_customers
    .groupby("customer_name")["sales"]
    .sum()
    .reset_index()
    .sort_values("sales", ascending=False)
)

plt.bar(
    customer_revenue["customer_name"],
    customer_revenue["sales"]
)

plt.title("Revenue by Customer")
plt.xlabel("Customer")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.show()

connection.close()