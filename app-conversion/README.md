# ADBC: Python to Rust

This demonstrates how ADBC provides a consistent API across databases and languages. The same mental model applies whether you're using Python or Rust, PostgreSQL or DuckDB.

## The Progression

1. **Python + PostgreSQL** - Query a PostgreSQL database
2. **Python + DuckDB** - Same code pattern, different database
3. **Rust + DuckDB** - Same pattern, different language

## Setup

Install ADBC drivers:

```bash
dbc install postgresql
dbc install duckdb
```

Start PostgreSQL (for the first example):

```bash
docker run --name postgres-local -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 -d postgres
```

## Running the Examples

### 1. Python + PostgreSQL

```bash
cd python-postgres
uv run --with adbc-driver-manager --with pyarrow --with pandas python app.py
```

### 2. Python + DuckDB

```bash
cd python-duckdb
uv run --with adbc-driver-manager --with pyarrow --with pandas python setup_db.py
uv run --with adbc-driver-manager --with pyarrow --with pandas python app.py
```

### 3. Rust + DuckDB

```bash
cd rust-duckdb
cargo run
```

(Uses the same `sales.duckdb` file created by the Python setup)

## Code Comparison

### db.py (Python + PostgreSQL)

```python
from adbc_driver_manager import dbapi

CONN_STR = "postgresql://postgres@localhost:5432/postgres"

def query(sql):
    with dbapi.connect(driver="postgresql", db_kwargs={"uri": CONN_STR}) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetch_df()
```

### db.py (Python + DuckDB)

```python
from adbc_driver_manager import dbapi

def query(sql):
    with dbapi.connect(driver="duckdb", db_kwargs={"path": "sales.duckdb"}) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetch_df()
```

**The only difference is `driver="postgresql"` → `driver="duckdb"` and the connection options.**

### db.rs (Rust + DuckDB)

```rust
use adbc_core::options::{AdbcVersion, OptionDatabase};
use adbc_core::{Connection, Database, Driver, Statement, LOAD_FLAG_DEFAULT};
use adbc_driver_manager::ManagedDriver;

pub fn query(sql: &str) -> Vec<RecordBatch> {
    let mut driver = ManagedDriver::load_from_name("duckdb", None, AdbcVersion::default(), LOAD_FLAG_DEFAULT, None)?;
    let opts = [(OptionDatabase::Uri, DB_PATH.into())];
    let db = driver.new_database_with_opts(opts)?;
    let mut conn = db.new_connection()?;
    let mut stmt = conn.new_statement()?;
    stmt.set_sql_query(sql)?;
    stmt.execute()?.collect()
}
```

**Same pattern: load driver → open database → create connection → execute statement.**

## Key Takeaways

1. **Database-agnostic**: Swap `driver="postgresql"` for `driver="duckdb"` - same API
2. **Language-portable**: The concepts (driver, database, connection, statement) map directly from Python to Rust
3. **Arrow-native**: Results come back as Arrow data (DataFrame in Python, RecordBatch in Rust) - efficient for analytics
4. **Driver management**: `dbc install <driver>` works the same regardless of language
