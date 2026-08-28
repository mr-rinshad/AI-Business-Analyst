from analysis.llm_client import ask_llm


def generate_investigation_answer(
    question,
    investigation
):

    prompt = f"""
You are a professional Business Analyst.

Answer the user's question using ONLY the evidence
provided below.

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

3. Clearly distinguish between correlation and evidence.

4. Identify the largest contributors to the revenue change.

5. Mention the overall revenue change and percentage change.

6. Mention important category or product changes.

7. Mention important customer changes.

8. Mention important region or segment changes.

9. Keep the answer concise but useful.

10. Do not mention Python, Pandas, SQL,
    or internal system details.

Write the answer as a professional business analyst.
"""

    return ask_llm(prompt).strip()