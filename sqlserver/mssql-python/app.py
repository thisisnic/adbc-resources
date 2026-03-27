"""
Connects to a SQL database using mssql-python
"""

from os import getenv
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()
print(repr(getenv("SQL_CONNECTION_STRING")))
conn = connect(getenv("SQL_CONNECTION_STRING"))

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



