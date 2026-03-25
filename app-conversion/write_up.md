# Converting a Python App to Rust with ADBC

*Written by Claude, with the help of the ADBC skill for Claude Code.*

This write-up documents converting a simple database query app from Python to Rust using ADBC (Arrow Database Connectivity). The goal was to demonstrate how ADBC's consistent API makes it easy to port code between languages and databases.

## The Starting Point

We started with a Python app using ADBC to query a PostgreSQL database:

```python
from adbc_driver_manager import dbapi

def query(sql):
    with dbapi.connect(driver="postgresql", db_kwargs={"uri": CONN_STR}) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetch_df()
```

Simple enough - connect to PostgreSQL, execute a query, return a DataFrame.

## Step 1: Switching Databases (PostgreSQL → DuckDB)

The first thing ADBC makes easy is switching databases. To move from PostgreSQL to DuckDB, we literally just changed the driver name and connection options:

```python
# Before (PostgreSQL)
dbapi.connect(driver="postgresql", db_kwargs={"uri": "postgresql://..."})

# After (DuckDB)
dbapi.connect(driver="duckdb", db_kwargs={"path": "sales.duckdb"})
```

That's it. The rest of the code - cursor creation, query execution, fetching results - stays identical. This is the database-agnostic promise of ADBC in action.

## Step 2: Switching Languages (Python → Rust)

Now the interesting part: porting to Rust. Here's what the equivalent Rust code looks like:

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

Yes, it's more verbose - Rust is explicit about everything. But look at the structure:

| Python | Rust |
|--------|------|
| `dbapi.connect(driver="duckdb", ...)` | `ManagedDriver::load_from_name("duckdb", ...)` |
| `conn.cursor()` | `conn.new_statement()` |
| `cur.execute(sql)` | `stmt.set_sql_query(sql)` then `stmt.execute()` |
| `cur.fetch_df()` | `reader.collect()` |

The mental model is the same: **driver → database → connection → statement → results**.

## What Made This Easy

### 1. The ADBC Skill

The Claude Code ADBC skill answered specific questions as they came up:

**"How do I install a driver?"**
The skill pointed to `dbc install <driver>` rather than pip/cargo packages. This is the preferred way since it works across languages.

**"What crates do I need for Rust?"**
The skill specified `adbc_core` and `adbc_driver_manager`, and warned about Arrow version mismatches - you need to match the Arrow version that the ADBC crates depend on (found via `cargo tree | grep arrow`).

**"How do I connect to DuckDB?"**
The skill showed the connection options: use `path` for a file or omit for in-memory. For PostgreSQL, it provided the URI format.

**"What does the Rust code look like?"**
The skill provided a complete working example showing the driver → database → connection → statement → execute flow, including imports and error handling.

Without the skill, I'd have been piecing together information from multiple doc sites (Arrow ADBC docs, crates.io, DuckDB docs, etc.).

### 2. Arrow-Native Data

Both Python and Rust return Arrow-format data:
- Python: `fetch_df()` returns a pandas DataFrame (via Arrow)
- Rust: `execute()` returns `RecordBatch` (Arrow's native format)

No serialization/deserialization between database and application. The data flows in columnar Arrow format throughout.

### 3. Shared Driver Infrastructure

Both languages use the same underlying drivers installed via `dbc`:

```bash
dbc install postgresql
dbc install duckdb
```

The Rust code literally loads the same driver binary that Python uses.

## Lessons Learned

### Rust is more explicit (as expected)

The Rust version has more lines, but that's just Rust - explicit error handling, explicit types. The ADBC API maps cleanly between languages and the pattern is identical.

### DuckDB is a better showcase than PostgreSQL

For Rust + ADBC, DuckDB is nicer because:
- Native Arrow support (no type conversion overhead)
- File-based (no Docker/server setup)
- The ADBC driver is well-maintained

### The pattern matters more than the syntax

Once you understand "driver → database → connection → statement → execute", you can write ADBC code in any language. The syntax differs but the concepts are portable.

## Final Structure

```
app-conversion/
├── python-postgres/    # Python + PostgreSQL
│   ├── app.py
│   └── db.py
├── python-duckdb/      # Python + DuckDB
│   ├── app.py
│   ├── db.py
│   └── setup_db.py
├── rust-duckdb/        # Rust + DuckDB
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs
│       └── db.rs
├── README.md           # Quick start instructions
└── write_up.md         # This document
```

## Conclusion

ADBC delivers on its promise of database-agnostic, language-portable database connectivity. The progression from Python+PostgreSQL to Python+DuckDB to Rust+DuckDB was straightforward, with each step requiring minimal changes.

The ADBC skill accelerated this by providing correct, working code patterns for each combination. Rather than piecing together docs and Stack Overflow answers, the skill gave me the right incantation immediately.

For analytics workloads where Arrow-native data flow matters, ADBC is a solid choice. The consistency across databases and languages makes it worth the slightly more verbose API.
