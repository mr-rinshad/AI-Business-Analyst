import os
import mysql.connector # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

print("Database connected successfully!")

connection.close()