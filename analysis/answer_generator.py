from analysis.llm_client import ask_llm


def generate_answer(question, sql, result):

    prompt = f"""
You are an AI Business Analyst.

Answer the user's business question using ONLY
the database result provided below.

USER QUESTION:
{question}

SQL QUERY:
{sql}

DATABASE RESULT:
{result}

RULES:

1. Give a clear and concise business answer.
2. Use the actual values from the database result.
3. Do not invent information.
4. Do not claim a reason unless the data supports it.
5. If the result contains multiple rows, summarize the important findings.
6. Use simple business language.
7. Mention important numbers and percentages when available.
8. Do not mention Python, Pandas, SQL, or the AI system.
9. If there is insufficient data to answer the question, clearly say so.

ANSWER:
"""

    answer = ask_llm(prompt)

    return answer.strip()


if __name__ == "__main__":

    question = "What is our total revenue?"

    sql = """
    SELECT SUM(sales) AS total_revenue
    FROM orders;
    """

    result = """
       total_revenue
    0       409350.0
    """

    answer = generate_answer(
        question,
        sql,
        result
    )

    print("Answer:")
    print(answer)