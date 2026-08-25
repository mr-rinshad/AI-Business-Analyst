MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}


def detect_month(question):

    question_lower = question.lower()

    for month_name, month_number in MONTHS.items():

        if month_name in question_lower:

            return month_number

    return None


def get_previous_month(month):

    if month <= 1:
        return None

    return month - 1


def get_investigation_months(question):

    current_month = detect_month(question)

    if current_month is None:

        return None, None

    previous_month = get_previous_month(
        current_month
    )

    return previous_month, current_month


if __name__ == "__main__":

    questions = [
        "Why did revenue drop in February?",
        "Why did revenue drop in March?",
        "Why did revenue drop in January?",
        "Why did sales decrease?"
    ]

    for question in questions:

        previous_month, current_month = (
            get_investigation_months(question)
        )

        print(question)

        print(
            "Previous:",
            previous_month
        )

        print(
            "Current:",
            current_month
        )

        print("-" * 40)