"""
Connects to a SQL database using mssql-python
"""

from os import getenv
from dotenv import load_dotenv
from adbc_driver_manager import dbapi

load_dotenv()

conn = dbapi.connect(
  driver="mssql",
  db_kwargs={
      "uri": f'mssql://{getenv("SQL_UID")}:{getenv("SQL_PASSWORD")}@localhost:1433'
  }
)




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



