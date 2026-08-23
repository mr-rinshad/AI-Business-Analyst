import pandas as pd
from analysis.analysis_engine import (
    load_orders,
    analyze_monthly_revenue,
    analyze_monthly_category_revenue,
    get_connection
)

def analyze_revenue_drop():

    orders = load_orders()

    monthly_revenue = analyze_monthly_revenue(
        orders
    )

    return monthly_revenue

def find_largest_revenue_drop(monthly_revenue):

    valid_changes = monthly_revenue.dropna(
        subset=["revenue_change"]
    )

    if valid_changes.empty:
        return None

    largest_drop = valid_changes.loc[
        valid_changes["revenue_change"].idxmin()
    ]

    return largest_drop


def get_category_changes(
    orders,
    previous_month,
    current_month
):

    monthly_category = (
        analyze_monthly_category_revenue(
            orders
        )
    )

    previous = monthly_category[
        monthly_category["month"] == previous_month
    ]

    current = monthly_category[
        monthly_category["month"] == current_month
    ]

    comparison = previous.merge(
        current,
        on="category",
        how="outer",
        suffixes=("_previous", "_current")
    )

    comparison["revenue_previous"] = (
        comparison["revenue_previous"]
        .fillna(0)
    )

    comparison["revenue_current"] = (
        comparison["revenue_current"]
        .fillna(0)
    )

    comparison["revenue_change"] = (
        comparison["revenue_current"]
        -
        comparison["revenue_previous"]
    )

    return comparison.sort_values(
        "revenue_change"
    )


def compare_revenue(
    monthly_revenue,
    previous_month,
    current_month
):

    previous = monthly_revenue[
        monthly_revenue["month"] == previous_month
    ]

    current = monthly_revenue[
        monthly_revenue["month"] == current_month
    ]

    if previous.empty or current.empty:
        return None

    previous_revenue = previous.iloc[0]["revenue"]
    current_revenue = current.iloc[0]["revenue"]

    revenue_change = (
        current_revenue - previous_revenue
    )

    percentage_change = (
        revenue_change / previous_revenue
    ) * 100

    return {
        "previous_month": previous_month,
        "current_month": current_month,
        "previous_revenue": previous_revenue,
        "current_revenue": current_revenue,
        "revenue_change": revenue_change,
        "percentage_change": percentage_change
    }

def calculate_category_contribution(
    category_changes,
    total_revenue_change
):

    result = category_changes.copy()

    if total_revenue_change >= 0:
        return result

    result["contribution"] = (
        result["revenue_change"]
        / total_revenue_change
    ) * 100

    return result


def find_top_declining_category(
    category_contribution
):

    declining = category_contribution[
        category_contribution["revenue_change"] < 0
    ]

    if declining.empty:
        return None

    return declining.iloc[0]

def analyze_customer_changes(
    orders,
    previous_month,
    current_month
):

    connection = get_connection()

    customers_query = """
        SELECT *
        FROM customers
    """

    customers_df = pd.read_sql(
        customers_query,
        connection
    )

    connection.close()

    orders = orders.copy()

    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    )

    orders["month"] = (
        orders["order_date"].dt.month
    )

    merged = orders.merge(
        customers_df,
        on="customer_id",
        how="left"
    )

    previous = (
        merged[
            merged["month"] == previous_month
        ]
        .groupby("customer_name")["sales"]
        .sum()
        .reset_index()
        .rename(
            columns={"sales": "revenue_previous"}
        )
    )

    current = (
        merged[
            merged["month"] == current_month
        ]
        .groupby("customer_name")["sales"]
        .sum()
        .reset_index()
        .rename(
            columns={"sales": "revenue_current"}
        )
    )

    comparison = previous.merge(
        current,
        on="customer_name",
        how="outer"
    )

    comparison["revenue_previous"] = (
        comparison["revenue_previous"]
        .fillna(0)
    )

    comparison["revenue_current"] = (
        comparison["revenue_current"]
        .fillna(0)
    )

    comparison["revenue_change"] = (
        comparison["revenue_current"]
        -
        comparison["revenue_previous"]
    )

    return comparison.sort_values(
        "revenue_change"
    )

def calculate_customer_contribution(
    customer_changes,
    total_revenue_change
):

    result = customer_changes.copy()

    if total_revenue_change >= 0:
        return result

    result["contribution"] = (
        result["revenue_change"]
        / total_revenue_change
    ) * 100

    return result

def find_top_declining_customer(
    customer_contribution
):

    declining = customer_contribution[
        customer_contribution["revenue_change"] < 0
    ]

    if declining.empty:
        return None

    return declining.iloc[0]


def analyze_order_metrics(
    orders,
    previous_month,
    current_month
):

    orders = orders.copy()

    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    )

    orders["month"] = (
        orders["order_date"].dt.month
    )

    previous = orders[
        orders["month"] == previous_month
    ]

    current = orders[
        orders["month"] == current_month
    ]

    previous_orders = len(previous)
    current_orders = len(current)

    previous_revenue = previous["sales"].sum()
    current_revenue = current["sales"].sum()

    previous_aov = (
        previous_revenue / previous_orders
        if previous_orders > 0
        else 0
    )

    current_aov = (
        current_revenue / current_orders
        if current_orders > 0
        else 0
    )

    return {
        "previous_orders": previous_orders,
        "current_orders": current_orders,
        "order_change": (
            current_orders - previous_orders
        ),
        "previous_aov": previous_aov,
        "current_aov": current_aov,
        "aov_change": (
            current_aov - previous_aov
        )
    }

def investigate_revenue_drop(
    previous_month,
    current_month
):

    orders = load_orders()

    monthly_revenue = analyze_monthly_revenue(
        orders
    )

    revenue_comparison = compare_revenue(
        monthly_revenue,
        previous_month,
        current_month
    )

    if revenue_comparison is None:
        return None

    total_change = (
        revenue_comparison["revenue_change"]
    )

    category_changes = get_category_changes(
        orders,
        previous_month,
        current_month
    )

    category_contribution = (
        calculate_category_contribution(
            category_changes,
            total_change
        )
    )

    customer_changes = analyze_customer_changes(
        orders,
        previous_month,
        current_month
    )

    customer_contribution = (
        calculate_customer_contribution(
            customer_changes,
            total_change
        )
    )

    order_metrics = analyze_order_metrics(
        orders,
        previous_month,
        current_month
    )

    return {
        "revenue_comparison": revenue_comparison,
        "category_analysis": category_contribution,
        "customer_analysis": customer_contribution,
        "order_metrics": order_metrics
    }


if __name__ == "__main__":

    investigation = investigate_revenue_drop(
        1,
        2
    )

    print("\nRevenue Comparison:")
    print(
        investigation["revenue_comparison"]
    )

    print("\nCategory Analysis:")
    print(
        investigation["category_analysis"]
    )

    print("\nCustomer Analysis:")
    print(
        investigation["customer_analysis"]
    )

    print("\nOrder Metrics:")
    print(
        investigation["order_metrics"]
    )