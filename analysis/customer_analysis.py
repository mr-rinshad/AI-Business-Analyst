from analysis.analysis_engine import get_connection


# --------------------------------
# Calculate Percentage Change
# --------------------------------

def calculate_percentage_change(
    previous,
    current
):

    if previous == 0:
        return None

    return (
        (current - previous)
        / previous
    ) * 100


# --------------------------------
# Get Customer Changes
# --------------------------------

def get_customer_changes(
    connection,
    previous_month,
    current_month,
    metric="revenue"
):

    metric_columns = {

        "revenue": "o.sales",

        "sales": "o.sales",

        "profit": "o.profit",

        "quantity": "o.quantity"
    }


    if metric not in metric_columns:

        raise ValueError(
            f"Unsupported customer metric: {metric}"
        )


    column = metric_columns[metric]


    query = f"""

        SELECT

            c.customer_id,

            c.customer_name,

            c.region,

            c.segment,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN {column}
                        ELSE 0
                    END
                ),
                0
            ) AS previous_value,

            COALESCE(
                SUM(
                    CASE
                        WHEN MONTH(o.order_date) = %s
                        THEN {column}
                        ELSE 0
                    END
                ),
                0
            ) AS current_value

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

        ORDER BY
            c.customer_id

    """


    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        query,
        (
            previous_month,
            current_month,
            previous_month,
            current_month
        )
    )


    rows = cursor.fetchall()


    cursor.close()


    results = []


    for row in rows:

        previous_value = row[
            "previous_value"
        ]

        current_value = row[
            "current_value"
        ]


        change = (
            current_value
            -
            previous_value
        )


        percentage_change = (
            calculate_percentage_change(
                previous_value,
                current_value
            )
        )


        results.append({

            "customer_id":
                row["customer_id"],

            "customer_name":
                row["customer_name"],

            "region":
                row["region"],

            "segment":
                row["segment"],

            "previous_value":
                previous_value,

            "current_value":
                current_value,

            "change":
                change,

            "percentage_change":
                percentage_change

        })


    return results


# --------------------------------
# Identify Customer Drivers
# --------------------------------

def identify_customer_drivers(
    customer_changes
):

    declining = [

        row

        for row in customer_changes

        if row["change"] < 0

    ]


    growing = [

        row

        for row in customer_changes

        if row["change"] > 0

    ]


    declining.sort(
        key=lambda row:
        row["change"]
    )


    growing.sort(
        key=lambda row:
        row["change"],
        reverse=True
    )


    return {

        "declining_customers":
            declining[:5],

        "growing_customers":
            growing[:5]

    }


# --------------------------------
# Main Customer Analysis
# --------------------------------

def analyze_customers(
    previous_month,
    current_month,
    metric="revenue"
):

    connection = get_connection()


    try:

        customer_changes = (
            get_customer_changes(
                connection,
                previous_month,
                current_month,
                metric
            )
        )

    finally:

        connection.close()


    drivers = (
        identify_customer_drivers(
            customer_changes
        )
    )


    return {

        "metric": metric,

        "previous_month":
            previous_month,

        "current_month":
            current_month,

        "customers":
            customer_changes,

        "drivers":
            drivers

    }


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    result = analyze_customers(
        2,
        3,
        "revenue"
    )


    print(
        "\nCustomer Analysis:"
    )


    print(result)