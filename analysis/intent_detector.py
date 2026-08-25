def detect_intent(question):

    question_lower = question.lower()

    investigation_keywords = [
        "why",
        "reason",
        "cause",
        "decline",
        "drop",
        "decrease",
        "decreased",
        "fell",
        "fall",
        "down"
    ]

    for keyword in investigation_keywords:

        if keyword in question_lower:

            return "investigation"

    return "query"


if __name__ == "__main__":

    questions = [
        "What is our total revenue?",
        "Show revenue by month.",
        "Why did revenue drop in February?",
        "What caused the decrease in sales?"
    ]

    for question in questions:

        print(
            question,
            "→",
            detect_intent(question)
        )