from analysis.llm_client import ask_llm
from analysis.schema import DATABASE_SCHEMA


def generate_sql(question):

    prompt = f"""
You are an expert MySQL business analyst.

Your task is to convert a user's business question
into a valid MySQL SELECT query.

DATABASE SCHEMA:

{DATABASE_SCHEMA}

RULES:

1. Generate ONLY the SQL query.
2. Use MySQL syntax.
3. Do not use Markdown.
4. Do not explain the query.
5. Only use tables and columns from the provided schema.
6. Only generate read-only SELECT queries.
7. Never use INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, or RENAME.
8. Use meaningful aliases for calculated values.
9. If aggregation is required, use appropriate GROUP BY.
10. Do not invent tables or columns.

USER QUESTION:

{question}

SQL:
"""

    sql = ask_llm(prompt)

    return sql.strip()


if __name__ == "__main__":

    question = "Which category generated the highest revenue??"

    sql = generate_sql(question)

    print("Generated SQL:")
    print(sql)