from db import query

df = query("SELECT * FROM sales")
print(df)
