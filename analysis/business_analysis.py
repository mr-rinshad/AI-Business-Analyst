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

    question = question.lower().strip()

    months = {
        "january": 1,
        "jan": 1,

        "february": 2,
        "feb": 2,

        "march": 3,
        "mar": 3,

        "april": 4,
        "apr": 4,

        "may": 5,

        "june": 6,
        "jun": 6,

        "july": 7,
        "jul": 7,

        "august": 8,
        "aug": 8,

        "september": 9,
        "sep": 9,
        "sept": 9,

        "october": 10,
        "oct": 10,

        "november": 11,
        "nov": 11,

        "december": 12,
        "dec": 12
    }

    # Sort longer names first
    # so "march" is checked before "mar"
    month_names = sorted(
        months.keys(),
        key=len,
        reverse=True
    )

    for month_name in month_names:

        pattern = rf"\b{re.escape(month_name)}\b"

        if re.search(pattern, question):

            return months[month_name]

    return None

# --------------------------------
# Extract Year From Question
# --------------------------------

def extract_year(question):

    match = re.search(
        r"\b(20\d{2})\b",
        question
    )

    if match:

        return int(
            match.group(1)
        )

    return None

# --------------------------------
# Get Previous Month
# --------------------------------

def get_previous_month(month):

    if month == 1:
        return 12

    return month - 1


# --------------------------------
# Get Analysis Period
# --------------------------------

def get_analysis_period(question):

    current_month = extract_month(
        question
    )

    if current_month is None:

        return None

    current_year = extract_year(
        question
    )

    return {
        "current_month": current_month,
        "current_year": current_year
    }

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
# Detect Revenue Direction
# --------------------------------

def extract_revenue_direction(question):

    question = question.lower()

    if re.search(
        r"\b(decrease|decreased|decline|declined|drop|dropped|fall|fell|down)\b",
        question
    ):

        return "decrease"

    if re.search(
        r"\b(increase|increased|growth|grew|rise|rose|up)\b",
        question
    ):

        return "increase"

    return None

# --------------------------------
# Validate Revenue Direction
# --------------------------------

def validate_revenue_direction(
    question,
    comparison
):

    requested_direction = (
        extract_revenue_direction(
            question
        )
    )

    revenue_change = (
        comparison["revenue_change"]
    )

    if revenue_change > 0:

        actual_direction = "increase"

    elif revenue_change < 0:

        actual_direction = "decrease"

    else:

        actual_direction = "no_change"

    return {

        "requested_direction":
            requested_direction,

        "actual_direction":
            actual_direction,

        "matches":
            (
                requested_direction is None
                or requested_direction
                == actual_direction
            )
    }
# --------------------------------
# Test
# --------------------------------
if __name__ == "__main__":

    questions = [

        "Why did revenue change in March 2026?",

        "Why did revenue change in February 2025?",

        "Why did revenue change in April?"
    ]

    for question in questions:

        period = get_analysis_period(
            question
        )

        print(
            question,
            "->",
            period
        )