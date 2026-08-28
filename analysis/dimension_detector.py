# --------------------------------
# Detect Business Dimension
# --------------------------------

def detect_dimension(question):

    question_lower = question.lower().strip()

    # --------------------------------
    # Customer
    # --------------------------------

    if (
        "customer" in question_lower
        or "customers" in question_lower
        or "client" in question_lower
        or "clients" in question_lower
    ):

        return "customer"

    # --------------------------------
    # Product
    # --------------------------------

    if (
        "product" in question_lower
        or "products" in question_lower
        or "item" in question_lower
        or "items" in question_lower
    ):

        return "product"

    # --------------------------------
    # Category
    # --------------------------------

    if (
        "category" in question_lower
        or "categories" in question_lower
    ):

        return "category"

    # --------------------------------
    # Region
    # --------------------------------

    if (
        "region" in question_lower
        or "regions" in question_lower
        or "area" in question_lower
        or "areas" in question_lower
    ):

        return "region"

    # --------------------------------
    # Segment
    # --------------------------------

    if (
        "segment" in question_lower
        or "segments" in question_lower
    ):

        return "segment"

    # --------------------------------
    # Unknown
    # --------------------------------

    return None


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    questions = [

        "Which category generated the most revenue?",

        "Which product has the highest sales?",

        "Which customer generated the most revenue?",

        "Which region performs best?",

        "Show revenue by customer.",

        "Show profit by product.",

        "Show sales by region.",

        "Show revenue by segment.",

        "What is our total revenue?"

    ]

    for question in questions:

        dimension = detect_dimension(
            question
        )

        print(
            question,
            "→",
            dimension
        )