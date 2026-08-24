def select_chart(question, data):

    question_lower = question.lower()

    columns = data.columns.tolist()

    # Don't create charts for a single-value result
    if len(data) <= 1:

        return None

    # Time-based analysis
    if (
        "month" in question_lower
        or "monthly" in question_lower
        or "trend" in question_lower
        or "over time" in question_lower
    ):

        if len(columns) >= 2:

            return {
                "chart_type": "line",
                "x_column": columns[0],
                "y_column": columns[1],
                "title": "Trend Over Time"
            }

    # Category analysis
    if (
        "category" in question_lower
        or "categories" in question_lower
    ):

        if len(columns) >= 2:

            return {
                "chart_type": "bar",
                "x_column": columns[0],
                "y_column": columns[1],
                "title": "Revenue by Category"
            }

    # Customer analysis
    if (
        "customer" in question_lower
        or "customers" in question_lower
    ):

        if len(columns) >= 2:

            return {
                "chart_type": "bar",
                "x_column": columns[0],
                "y_column": columns[1],
                "title": "Revenue by Customer"
            }

    # Don't automatically create a chart
    # unless the question suggests comparison
    if (
        "compare" in question_lower
        or "show" in question_lower
        or "distribution" in question_lower
    ):

        if len(columns) >= 2:

            return {
                "chart_type": "bar",
                "x_column": columns[0],
                "y_column": columns[1],
                "title": "Business Analysis"
            }

    return None