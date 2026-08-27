from analysis.analysis_engine import get_connection


# --------------------------------
# Get Monthly Metric
# --------------------------------

def get_monthly_metric(
    connection,
    month,
    metric
):

    metric_queries = {

        "revenue": """
            SELECT
                COALESCE(SUM(sales), 0) AS value
            FROM orders
            WHERE MONTH(order_date) = %s
        """,

        "sales": """
            SELECT
                COALESCE(SUM(sales), 0) AS value
            FROM orders
            WHERE MONTH(order_date) = %s
        """,

        "profit": """
            SELECT
                COALESCE(SUM(profit), 0) AS value
            FROM orders
            WHERE MONTH(order_date) = %s
        """,

        "quantity": """
            SELECT
                COALESCE(SUM(quantity), 0) AS value
            FROM orders
            WHERE MONTH(order_date) = %s
        """,

        "orders": """
            SELECT
                COUNT(order_id) AS value
            FROM orders
            WHERE MONTH(order_date) = %s
        """,

        "average_order_value": """
            SELECT
                COALESCE(
                    SUM(sales) /
                    NULLIF(COUNT(order_id), 0),
                    0
                ) AS value
            FROM orders
            WHERE MONTH(order_date) = %s
        """
    }


    if metric not in metric_queries:

        raise ValueError(
            f"Unsupported metric: {metric}"
        )


    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        metric_queries[metric],
        (month,)
    )


    result = cursor.fetchone()


    cursor.close()


    return result["value"]


# --------------------------------
# Compare Metric Between Months
# --------------------------------

def compare_metric(
    previous_month,
    current_month,
    metric
):

    connection = get_connection()

    try:

        previous_value = get_monthly_metric(
            connection,
            previous_month,
            metric
        )

        current_value = get_monthly_metric(
            connection,
            current_month,
            metric
        )

    finally:

        connection.close()


    change = (
        current_value
        -
        previous_value
    )


    if previous_value == 0:

        percentage_change = None

    else:

        percentage_change = (
            change / previous_value
        ) * 100


    return {

        "metric": metric,

        "previous_month": previous_month,

        "current_month": current_month,

        "previous_value": previous_value,

        "current_value": current_value,

        "change": change,

        "percentage_change":
            percentage_change
    }


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    metrics = [

        "revenue",
        "sales",
        "profit",
        "quantity",
        "orders",
        "average_order_value"
    ]


    for metric in metrics:

        result = compare_metric(
            2,
            3,
            metric
        )

        print(
            f"\n{metric}:"
        )

        print(result)