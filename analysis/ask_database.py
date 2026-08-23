from analysis.sql_generator import generate_sql
from analysis.sql_executor import execute_sql


def ask_database(question):

    # Step 1: Convert question to SQL
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    # Step 2: Execute SQL safely
    result = execute_sql(sql)

    return result


if __name__ == "__main__":

    question = "What is our total profit?"

    result = ask_database(question)

    print("\nResult:")
    print(result)