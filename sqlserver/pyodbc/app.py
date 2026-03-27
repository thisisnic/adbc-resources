"""
Connects to a SQL database using mssql-python
"""

from os import getenv
from dotenv import load_dotenv
from pyodbc import connect

load_dotenv()

conn =connect(f'DSN=MSSQLServerDatabase;UID={getenv("SQL_UID")};PWD={getenv("SQL_PASSWORD")}')



SQL_QUERY = """
SELECT
*
FROM 
products;
"""

cursor = conn.cursor()
cursor.execute(SQL_QUERY)

rows = cursor.fetchall()
for row in rows:
    print(row)



