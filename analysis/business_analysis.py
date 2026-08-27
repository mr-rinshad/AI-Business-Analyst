import re

from analysis.analysis_engine import get_connection


# --------------------------------
# Calculate Percentage Change
# --------------------------------

def calculate_percentage_change(previous, current):

    if previous is None or current is None:
        return None

    if previous == 0:
        return None

    return (
        (current - previous) / previous
    ) * 100


# --------------------------------
# Extract Month From Question
# --------------------------------

def extract_month(question):

    question = question.lower()

    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    for month_name, month_number in months.items():

        if month_name in question:
            return month_number

    return None


# --------------------------------
# Get Previous Month
# --------------------------------

def get_previous_month(month):

    if month == 1:
        return 12

    return month - 1


# --------------------------------
# Get Monthly Metrics
# --------------------------------

def get_monthly_metrics(
    connection,
    month
):

    query = """
        SELECT

            COALESCE(
                SUM(sales),
                0
            ) AS revenue,

            COUNT(order_id)
            AS total_orders,

            COALESCE(
                SUM(quantity),
                0
            ) AS total_quantity,

            COALESCE(
                SUM(sales) /
                NULLIF(COUNT(order_id), 0),
                0
            ) AS average_order_value,

            COALESCE(
                SUM(profit),
                0
            ) AS total_profit

        FROM orders

        WHERE MONTH(order_date) = %s
    """

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        query,
        (month,)
    )

    result = cursor.fetchone()

    cursor.close()

    return result


# --------------------------------
# Compare Two Months
# --------------------------------

def compare_months(
    connection,
    previous_month,
    current_month
):

    previous = get_monthly_metrics(
        connection,
        previous_month
    )

    current = get_monthly_metrics(
        connection,
        current_month
    )

    if previous is None or current is None:
        return None

    revenue_change = (
        current["revenue"]
        -
        previous["revenue"]
    )

    revenue_percentage_change = (
        calculate_percentage_change(
            previous["revenue"],
            current["revenue"]
        )
    )

    orders_change = (
        current["total_orders"]
        -
        previous["total_orders"]
    )

    quantity_change = (
        current["total_quantity"]
        -
        previous["total_quantity"]
    )

    aov_change = (
        current["average_order_value"]
        -
        previous["average_order_value"]
    )

    profit_change = (
        current["total_profit"]
        -
        previous["total_profit"]
    )

    return {

        "previous": previous,

        "current": current,

        "revenue_change":
            revenue_change,

        "revenue_percentage_change":
            revenue_percentage_change,

        "orders_change":
            orders_change,

        "quantity_change":
            quantity_change,

        "aov_change":
            aov_change,

        "profit_change":
            profit_change
    }


# --------------------------------
# Category Changes
# --------------------------------

def get_category_changes(
    connection,
    previous_month,
    current_month
):

    query = """

        SELECT

            p.category,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS previous_revenue,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS current_revenue,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            )
            -
            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS revenue_change

        FROM orders o

        JOIN products p
            ON o.product_id = p.product_id

        WHERE MONTH(o.order_date)
        IN (%s, %s)

        GROUP BY p.category

        ORDER BY revenue_change ASC
    """

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        query,
        (
            previous_month,
            current_month,
            current_month,
            previous_month,
            previous_month,
            current_month
        )
    )

    result = cursor.fetchall()

    cursor.close()

    return result


# --------------------------------
# Identify Category Drivers
# --------------------------------

def identify_category_drivers(
    category_changes
):

    declining = [
        row
        for row in category_changes
        if row["revenue_change"] < 0
    ]

    increasing = [
        row
        for row in category_changes
        if row["revenue_change"] > 0
    ]

    declining.sort(
        key=lambda row:
        row["revenue_change"]
    )

    increasing.sort(
        key=lambda row:
        row["revenue_change"],
        reverse=True
    )

    return {

        "declining_categories":
            declining,

        "growing_categories":
            increasing
    }


# --------------------------------
# Customer Changes
# --------------------------------

def get_customer_changes(
    connection,
    previous_month,
    current_month
):

    query = """

        SELECT

            c.customer_id,

            c.customer_name,

            c.region,

            c.segment,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS previous_revenue,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS current_revenue,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            )
            -
            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS revenue_change

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE MONTH(o.order_date)
        IN (%s, %s)

        GROUP BY

            c.customer_id,
            c.customer_name,
            c.region,
            c.segment

        ORDER BY revenue_change ASC
    """

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        query,
        (
            previous_month,
            current_month,
            current_month,
            previous_month,
            previous_month,
            current_month
        )
    )

    result = cursor.fetchall()

    cursor.close()

    return result


# --------------------------------
# Identify Customer Drivers
# --------------------------------

def identify_customer_drivers(
    customer_changes
):

    declining = [
        row
        for row in customer_changes
        if row["revenue_change"] < 0
    ]

    increasing = [
        row
        for row in customer_changes
        if row["revenue_change"] > 0
    ]

    declining.sort(
        key=lambda row:
        row["revenue_change"]
    )

    increasing.sort(
        key=lambda row:
        row["revenue_change"],
        reverse=True
    )

    return {

        "declining_customers":
            declining[:5],

        "growing_customers":
            increasing[:5]
    }


# --------------------------------
# Product Changes
# --------------------------------

def get_product_changes(
    connection,
    previous_month,
    current_month
):

    query = """

        SELECT

            p.product_id,

            p.product_name,

            p.category,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS previous_revenue,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS current_revenue,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            )
            -
            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN o.sales
                        ELSE 0
                    END
                ),
                0
            ) AS revenue_change

        FROM orders o

        JOIN products p
            ON o.product_id = p.product_id

        WHERE MONTH(o.order_date)
        IN (%s, %s)

        GROUP BY

            p.product_id,
            p.product_name,
            p.category

        ORDER BY revenue_change ASC
    """

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        query,
        (
            previous_month,
            current_month,
            current_month,
            previous_month,
            previous_month,
            current_month
        )
    )

    result = cursor.fetchall()

    cursor.close()

    return result


# --------------------------------
# Identify Product Drivers
# --------------------------------

def identify_product_drivers(
    product_changes
):

    declining = [
        row
        for row in product_changes
        if row["revenue_change"] < 0
    ]

    increasing = [
        row
        for row in product_changes
        if row["revenue_change"] > 0
    ]

    declining.sort(
        key=lambda row:
        row["revenue_change"]
    )

    increasing.sort(
        key=lambda row:
        row["revenue_change"],
        reverse=True
    )

    return {

        "declining_products":
            declining[:5],

        "growing_products":
            increasing[:5]
    }


# --------------------------------
# Main Revenue Investigation
# --------------------------------

def investigate_revenue_change(
    previous_month,
    current_month
):

    connection = get_connection()

    try:

        comparison = compare_months(
            connection,
            previous_month,
            current_month
        )

        category_changes = get_category_changes(
            connection,
            previous_month,
            current_month
        )

        customer_changes = get_customer_changes(
            connection,
            previous_month,
            current_month
        )

        product_changes = get_product_changes(
            connection,
            previous_month,
            current_month
        )

        return {

            "comparison": comparison,

            "categories":
                identify_category_drivers(
                    category_changes
                ),

            "customers":
                identify_customer_drivers(
                    customer_changes
                ),

            "products":
                identify_product_drivers(
                    product_changes
                )
        }

    finally:

        connection.close()


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    question = "Why did revenue drop in March?"

    current_month = extract_month(
        question
    )

    previous_month = get_previous_month(
        current_month
    )

    print(
        "Question:",
        question
    )

    print(
        "Previous Month:",
        previous_month
    )

    print(
        "Current Month:",
        current_month
    )

    if current_month is not None:

        result = investigate_revenue_change(
            previous_month,
            current_month
        )

        print("\nRevenue Investigation:")

        print(result)