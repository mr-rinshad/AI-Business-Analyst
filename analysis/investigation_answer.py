from analysis.llm_client import ask_llm


def generate_investigation_answer(
    question,
    investigation,
    direction_check
):

    comparison = investigation["comparison"]

    categories = investigation["categories"]

    customers = investigation["customers"]

    products = investigation["products"]


    prompt = f"""
You are a professional Business Analyst.

Answer the user's business question using ONLY
the evidence provided below.

USER QUESTION:
{question}


REVENUE COMPARISON:
{comparison}


CATEGORY ANALYSIS:
{categories}


CUSTOMER ANALYSIS:
{customers}


PRODUCT ANALYSIS:
{products}

DIRECTION CHECK:
{direction_check}

RULES:

1. Use only the provided evidence.
2. Do not invent facts.
3. Do not assume causation without evidence.
4. Clearly distinguish between correlation and evidence.
5. Mention whether revenue increased or decreased.
6. Mention the revenue change and percentage change.
7. Identify the largest positive and negative contributors.
8. Mention important category, customer, or product changes.
9. Mention important changes in order volume,
   quantity, average order value, or profit when relevant.
10. If the user's assumption is incorrect, clearly correct it.
11. Keep the answer concise but useful.
12. Do not mention Python, Pandas, SQL, Gemini,
    or internal system details.

Write the answer as a professional business analyst.
"""

    return ask_llm(prompt).strip()