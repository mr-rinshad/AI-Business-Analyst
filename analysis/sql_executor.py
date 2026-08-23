import pandas as pd

from analysis.analysis_engine import get_connection
from analysis.sql_validator import validate_sql


def execute_sql(sql):

    if not validate_sql(sql):
        raise ValueError("Unsafe SQL query rejected.")

    connection = get_connection()

    try:
        result = pd.read_sql(sql, connection)

    finally:
        connection.close()

    return result


if __name__ == "__main__":

    sql = """
    SELECT SUM(sales) AS total_revenue
    FROM orders;
    """

    result = execute_sql(sql)

    print(result)