from analysis.llm_client import ask_llm


def generate_investigation_answer(
    question,
    investigation
):

    prompt = f"""
You are a professional Business Analyst.

Answer the user's question using ONLY the
evidence provided below.

USER QUESTION:
{question}

REVENUE COMPARISON:
{investigation["revenue_comparison"]}

CATEGORY ANALYSIS:
{investigation["category_analysis"]}

CUSTOMER ANALYSIS:
{investigation["customer_analysis"]}

ORDER METRICS:
{investigation["order_metrics"]}

RULES:

1. Do not invent facts.
2. Do not assume causation without evidence.
3. Clearly distinguish between correlation and evidence.
4. Identify the largest contributors to the revenue decline.
5. Mention the revenue change and percentage change.
6. Mention important category or customer declines.
7. Mention whether order volume or average order value changed.
8. Keep the answer concise but useful.
9. Do not mention Python, Pandas, SQL, or internal system details.

Write the answer as a professional business analyst.
"""

    return ask_llm(prompt).strip()


if __name__ == "__main__":

    from analysis.business_analysis import (
        investigate_revenue_drop
    )

    investigation = investigate_revenue_drop(
        1,
        2
    )

    question = (
        "Why did revenue drop in February?"
    )

    answer = generate_investigation_answer(
        question,
        investigation
    )

    print("\nBusiness Analysis:")
    print(answer)