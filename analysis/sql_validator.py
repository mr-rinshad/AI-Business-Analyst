import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "RENAME"
]


def validate_sql(sql):

    sql_upper = sql.upper().strip()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False

    # Only allow one SQL statement
    statements = [
        statement.strip()
        for statement in sql_upper.split(";")
        if statement.strip()
    ]

    if len(statements) != 1:
        return False

    # Check forbidden commands
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql_upper):
            return False

    return True


if __name__ == "__main__":

    safe_query = """
    SELECT SUM(sales)
    FROM orders;
    """

    dangerous_query = """
    DROP TABLE orders;
    """

    print(
        "Safe query:",
        validate_sql(safe_query)
    )

    print(
        "Dangerous query:",
        validate_sql(dangerous_query)
    )