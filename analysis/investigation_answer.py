from analysis.llm_client import ask_llm


def generate_investigation_answer(
    question,
    investigation
):

    prompt = f"""
You are a professional Business Analyst.

Answer the user's question using ONLY the
business evidence provided below.

USER QUESTION:
{question}

OVERALL COMPARISON:
{investigation["comparison"]}

CATEGORY ANALYSIS:
{investigation["categories"]}

PRODUCT ANALYSIS:
{investigation["products"]}

CUSTOMER ANALYSIS:
{investigation["customers"]}

REGION ANALYSIS:
{investigation["regions"]}

SEGMENT ANALYSIS:
{investigation["segments"]}


RULES:

1. Do not invent facts.

2. Do not assume causation without evidence.

3. Clearly distinguish correlation from evidence.

4. Identify the largest contributors to the
   revenue change.

5. Mention the revenue change and percentage change.

6. Mention important category changes.

7. Mention important product changes.

8. Mention important customer changes.

9. Mention important region or segment changes
   when relevant.

10. Mention changes in order volume,
    quantity, average order value,
    and profit when relevant.

11. Keep the answer concise but useful.

12. Do not mention Python, Pandas, SQL,
    or internal system details.

Write the answer as a professional
business analyst.
"""

    return ask_llm(prompt).strip()


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    from analysis.investigation_engine import (
        investigate_business_change
    )

    question = (
        "Why did revenue change "
        "from February to March?"
    )

    investigation = investigate_business_change(
        question,
        "revenue"
    )

    answer = generate_investigation_answer(
        question,
        investigation
    )

    print("\nBusiness Analysis:")
    print(answer)