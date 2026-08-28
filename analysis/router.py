# --------------------------------
# Dynamic Analysis Router
# --------------------------------


def route_analysis(
    intent,
    metric,
    dimension
):

    # --------------------------------
    # Investigation
    # --------------------------------

    if intent == "investigation":

        if dimension == "product":

            return "product_investigation"

        if dimension == "category":

            return "category_investigation"

        if dimension == "customer":

            return "customer_investigation"

        if dimension == "region":

            return "region_investigation"

        if dimension == "segment":

            return "segment_investigation"

        # No dimension specified
        # Use existing revenue investigation
        if metric == "revenue":

            return "revenue_investigation"

        if metric == "sales":

            return "sales_investigation"

        if metric == "profit":

            return "profit_investigation"

        if metric == "quantity":

            return "quantity_investigation"

        if metric == "orders":

            return "orders_investigation"

        if metric == "average_order_value":

            return "aov_investigation"

        return "general_investigation"


    # --------------------------------
    # Normal Query
    # --------------------------------

    if intent == "query":

        if dimension == "product":

            return "product_query"

        if dimension == "category":

            return "category_query"

        if dimension == "customer":

            return "customer_query"

        if dimension == "region":

            return "region_query"

        if dimension == "segment":

            return "segment_query"

        return "metric_query"


    # --------------------------------
    # Unknown
    # --------------------------------

    return "unknown"


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    test_cases = [

        (
            "investigation",
            "revenue",
            "category"
        ),

        (
            "investigation",
            "sales",
            "product"
        ),

        (
            "investigation",
            "profit",
            "customer"
        ),

        (
            "query",
            "revenue",
            "customer"
        ),

        (
            "query",
            "profit",
            "product"
        ),

        (
            "query",
            "revenue",
            None
        )

    ]


    for intent, metric, dimension in test_cases:

        route = route_analysis(
            intent,
            metric,
            dimension
        )

        print(
            f"Intent={intent}, "
            f"Metric={metric}, "
            f"Dimension={dimension}"
        )

        print(
            "→",
            route
        )

        print()