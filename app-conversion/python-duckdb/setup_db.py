"""Set up DuckDB with sample sales data."""

from db import execute

execute("DROP TABLE IF EXISTS sales")
execute("""
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        amount DECIMAL,
        sale_date DATE
    )
""")
execute("""
    INSERT INTO sales (id, product, amount, sale_date) VALUES
        (1, 'Widget', 100, '2024-01-15'),
        (2, 'Gadget', 250, '2024-01-16'),
        (3, 'Widget', 150, '2024-01-17'),
        (4, 'Gizmo', 300, '2024-01-18'),
        (5, 'Gadget', 200, '2024-01-19'),
        (6, 'Widget', 175, '2024-02-01'),
        (7, 'Gizmo', 225, '2024-02-02'),
        (8, 'Gadget', 275, '2024-02-03')
""")

print("Database setup complete!")
