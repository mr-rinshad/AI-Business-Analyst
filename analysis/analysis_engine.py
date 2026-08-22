import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


def load_orders():
    connection = get_connection()

    query = "SELECT * FROM orders"

    df = pd.read_sql(query, connection)

    connection.close()

    return df

def calculate_total_revenue(df):

    total_revenue = df["sales"].sum()

    return total_revenue

def calculate_total_profit(df):

    total_profit = df["profit"].sum()

    return total_profit

def calculate_total_orders(df):

    total_orders = df["order_id"].count()

    return total_orders

def calculate_average_order_value(df):

    total_revenue = df["sales"].sum()
    total_orders = df["order_id"].count()

    average_order_value = total_revenue / total_orders

    return average_order_value

def analyze_monthly_revenue(df):

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["month"] = df["order_date"].dt.month

    monthly_revenue = (
        df.groupby("month")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"sales": "revenue"})
    )

    monthly_revenue["revenue_change"] = (
        monthly_revenue["revenue"]
        .pct_change()
        * 100
    )

    return monthly_revenue

def analyze_category_revenue(df):

    connection = get_connection()

    products_query = "SELECT * FROM products"

    products_df = pd.read_sql(
        products_query,
        connection
    )

    connection.close()

    merged_df = df.merge(
        products_df,
        on="product_id",
        how="left"
    )

    category_revenue = (
        merged_df
        .groupby("category")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"sales": "revenue"})
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    return category_revenue


def analyze_customer_revenue(df):

    connection = get_connection()

    customers_query = "SELECT * FROM customers"

    customers_df = pd.read_sql(
        customers_query,
        connection
    )

    connection.close()

    merged_df = df.merge(
        customers_df,
        on="customer_id",
        how="left"
    )

    customer_revenue = (
        merged_df
        .groupby("customer_name")["sales"]
        .sum()
        .reset_index()
        .rename(columns={"sales": "revenue"})
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    return customer_revenue



if __name__ == "__main__":

    orders = load_orders()

    customer_revenue = analyze_customer_revenue(orders)

    print("\nCustomer Revenue:")
    print(customer_revenue)