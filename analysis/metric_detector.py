# --------------------------------
# Detect Business Metric
# --------------------------------

def detect_metric(question):

    question_lower = question.lower().strip()

    # --------------------------------
    # Average Order Value
    # --------------------------------

    if (
        "average order value" in question_lower
        or "aov" in question_lower
        or "average order" in question_lower
    ):

        return "average_order_value"

    # --------------------------------
    # Revenue
    # --------------------------------

    if (
        "revenue" in question_lower
        or "turnover" in question_lower
    ):

        return "revenue"

    # --------------------------------
    # Profit
    # --------------------------------

    if (
        "profit" in question_lower
        or "earnings" in question_lower
    ):

        return "profit"

    # --------------------------------
    # Orders
    # --------------------------------

    if (
        "orders" in question_lower
        or "order count" in question_lower
        or "number of orders" in question_lower
    ):

        return "orders"

    # --------------------------------
    # Quantity
    # --------------------------------

    if (
        "quantity" in question_lower
        or "units sold" in question_lower
        or "units" in question_lower
    ):

        return "quantity"

    # --------------------------------
    # Sales
    # --------------------------------

    if (
        "sales" in question_lower
        or "sales amount" in question_lower
    ):

        return "sales"

    # --------------------------------
    # Unknown
    # --------------------------------

    return None


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    questions = [

        "What is our total revenue?",

        "Show me total sales.",

        "How much profit did we make?",

        "How many orders did we receive?",

        "What is the total order count?",

        "How many units did we sell?",

        "What is our average order value?",

        "What is the AOV?",

        "Show me customer information."
    ]

    for question in questions:

        metric = detect_metric(
            question
        )

        print(
            question,
            "→",
            metric
        )