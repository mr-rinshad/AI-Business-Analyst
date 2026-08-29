import re


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


def extract_months(question):

    question_lower = question.lower()

    found_months = []

    for month_name, month_number in MONTHS.items():

        if re.search(
            rf"\b{month_name}\b",
            question_lower
        ):

            found_months.append(
                (month_name, month_number)
            )

    return found_months


def get_investigation_months(question):

    months = extract_months(question)

    if len(months) < 2:

        raise ValueError(
            "Please specify two months for comparison."
        )

    if len(months) > 2:

        raise ValueError(
            "Please specify exactly two months for comparison."
        )

    previous_month = months[0][1]

    current_month = months[1][1]

    return previous_month, current_month


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    questions = [

        "Why did revenue change from February to March?",

        "Compare revenue between January and February.",

        "Why did sales decrease from March to April."

    ]

    for question in questions:

        print(
            question,
            "→",
            get_investigation_months(question)
        )