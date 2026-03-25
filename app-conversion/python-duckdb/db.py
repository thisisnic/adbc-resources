from adbc_driver_manager import dbapi

def query(sql):
    with dbapi.connect(driver="duckdb", db_kwargs={"path": "sales.duckdb"}) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetch_df()


def execute(sql):
    with dbapi.connect(driver="duckdb", db_kwargs={"path": "sales.duckdb"}) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
