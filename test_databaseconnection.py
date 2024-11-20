import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the credentials from the .env file
server = os.getenv("DB_SERVER")  # Includes the port, e.g., "your_server_name,1433"
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Define the connection string
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Test the connection and fetch data
try:
    # Connect to the database
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        # Execute the SQL query
        query = "SELECT TOP 5 * FROM sales.order_items"
        cursor.execute(query)
        # Fetch and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)
except pyodbc.Error as e:
    print("Error connecting to database:", e)
