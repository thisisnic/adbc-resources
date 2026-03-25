from adbc_driver_manager import dbapi

CONN_STR = "postgresql://postgres@localhost:5432/postgres"

def query(sql):
    with dbapi.connect(driver="postgresql", db_kwargs={"uri": CONN_STR}) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetch_df()
