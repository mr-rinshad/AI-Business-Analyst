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
# Get Segment Changes
# --------------------------------

def get_segment_changes(
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
            f"Unsupported segment metric: {metric}"
        )


    column = metric_columns[metric]


    query = f"""

        SELECT

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
            c.segment

        ORDER BY
            c.segment

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
# Identify Segment Drivers
# --------------------------------

def identify_segment_drivers(
    segment_changes
):

    declining = [

        row

        for row in segment_changes

        if row["change"] < 0

    ]


    growing = [

        row

        for row in segment_changes

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

        "declining_segments":
            declining,

        "growing_segments":
            growing

    }


# --------------------------------
# Main Segment Analysis
# --------------------------------

def analyze_segments(
    previous_month,
    current_month,
    metric="revenue"
):

    connection = get_connection()


    try:

        segment_changes = (
            get_segment_changes(
                connection,
                previous_month,
                current_month,
                metric
            )
        )

    finally:

        connection.close()


    drivers = (
        identify_segment_drivers(
            segment_changes
        )
    )


    return {

        "metric": metric,

        "previous_month":
            previous_month,

        "current_month":
            current_month,

        "segments":
            segment_changes,

        "drivers":
            drivers

    }


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    result = analyze_segments(
        2,
        3,
        "revenue"
    )


    print(
        "\nSegment Analysis:"
    )


    print(result)