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
# Get Category Changes
# --------------------------------

def get_category_changes(
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
            f"Unsupported category metric: {metric}"
        )


    column = metric_columns[metric]


    query = f"""

        SELECT

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
            p.category

        ORDER BY
            p.category

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
# Identify Category Drivers
# --------------------------------

def identify_category_drivers(
    category_changes
):

    declining = [

        row

        for row in category_changes

        if row["change"] < 0

    ]


    growing = [

        row

        for row in category_changes

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

        "declining_categories":
            declining,

        "growing_categories":
            growing

    }


# --------------------------------
# Main Category Analysis
# --------------------------------

def analyze_categories(
    previous_month,
    current_month,
    metric="revenue"
):

    connection = get_connection()


    try:

        category_changes = (
            get_category_changes(
                connection,
                previous_month,
                current_month,
                metric
            )
        )

    finally:

        connection.close()


    drivers = (
        identify_category_drivers(
            category_changes
        )
    )


    return {

        "metric": metric,

        "previous_month":
            previous_month,

        "current_month":
            current_month,

        "categories":
            category_changes,

        "drivers":
            drivers

    }


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    result = analyze_categories(
        2,
        3,
        "revenue"
    )


    print(
        "\nCategory Analysis:"
    )


    print(result)