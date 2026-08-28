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
# Get Product Changes
# --------------------------------

def get_product_changes(
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
            f"Unsupported product metric: {metric}"
        )


    column = metric_columns[metric]


    query = f"""

        SELECT

            p.product_id,

            p.product_name,

            p.category,

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

        JOIN products p

            ON o.product_id = p.product_id

        WHERE MONTH(o.order_date)
        IN (%s, %s)

        GROUP BY

            p.product_id,
            p.product_name,
            p.category

        ORDER BY
            p.product_id

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

            "product_id":
                row["product_id"],

            "product_name":
                row["product_name"],

            "category":
                row["category"],

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
# Identify Product Drivers
# --------------------------------

def identify_product_drivers(
    product_changes
):

    declining = [

        row

        for row in product_changes

        if row["change"] < 0

    ]


    growing = [

        row

        for row in product_changes

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

        "declining_products":
            declining[:5],

        "growing_products":
            growing[:5]

    }


# --------------------------------
# Main Product Analysis
# --------------------------------

def analyze_products(
    previous_month,
    current_month,
    metric="revenue"
):

    connection = get_connection()


    try:

        product_changes = (
            get_product_changes(
                connection,
                previous_month,
                current_month,
                metric
            )
        )

    finally:

        connection.close()


    drivers = (
        identify_product_drivers(
            product_changes
        )
    )


    return {

        "metric": metric,

        "previous_month":
            previous_month,

        "current_month":
            current_month,

        "products":
            product_changes,

        "drivers":
            drivers

    }


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    result = analyze_products(
        2,
        3,
        "revenue"
    )


    print(
        "\nProduct Analysis:"
    )


    print(result)