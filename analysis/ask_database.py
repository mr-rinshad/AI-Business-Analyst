from analysis.sql_generator import generate_sql
from analysis.sql_executor import execute_sql
from analysis.answer_generator import generate_answer
from analysis.visualization_engine import visualize_result


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

    # Step 4: Create visualization
    chart_path = visualize_result(
        question,
        result
    )

    return {
        "answer": answer,
        "data": result,
        "chart": chart_path
    }


if __name__ == "__main__":

    question = "Show revenue by category"

    response = ask_database(question)

    print("\nBusiness Answer:")
    print(response["answer"])

    print("\nChart:")
    print(response["chart"])