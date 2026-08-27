# --------------------------------
# Detect Business Question Intent
# --------------------------------

def detect_intent(question):

    question_lower = question.lower().strip()

    # --------------------------------
    # Investigation Keywords
    # --------------------------------

    investigation_keywords = [

        "why",

        "reason",

        "cause",

        "caused",

        "because",

        "decline",

        "declined",

        "drop",

        "dropped",

        "decrease",

        "decreased",

        "fell",

        "fall",

        "down",

        "lower",

        "decreased",

        "reduced",

        "reduction",

        "lost",

        "loss"
    ]

    # --------------------------------
    # Check Investigation Intent
    # --------------------------------

    for keyword in investigation_keywords:

        if keyword in question_lower:

            return "investigation"

    # --------------------------------
    # Default Intent
    # --------------------------------

    return "query"


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    questions = [

        "What is our total revenue?",

        "Show revenue by month.",

        "Why did revenue drop in February?",

        "What caused the decrease in sales?",

        "Why was profit lower in March?",

        "Why did sales fall?",

        "Which product has the highest sales?",

        "Which customer generated the most revenue?"

    ]

    for question in questions:

        print(
            question,
            "→",
            detect_intent(question)
        )