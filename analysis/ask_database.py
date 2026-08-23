from analysis.sql_generator import generate_sql
from analysis.sql_executor import execute_sql
from analysis.answer_generator import generate_answer


def ask_database(question):

    # Step 1: Generate SQL
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    # Step 2: Execute SQL
    result = execute_sql(sql)

    print("\nDatabase Result:")
    print(result)

    # Step 3: Generate business answer
    answer = generate_answer(
        question,
        sql,
        result
    )

    return answer


if __name__ == "__main__":

    question = "Which category generated the highest revenue?"

    answer = ask_database(question)

    print("\nBusiness Answer:")
    print(answer)