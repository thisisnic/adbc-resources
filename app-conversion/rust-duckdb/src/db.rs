use adbc_core::options::{AdbcVersion, OptionDatabase};
use adbc_core::{Connection, Database, Driver, Statement, LOAD_FLAG_DEFAULT};
use adbc_driver_manager::ManagedDriver;
use arrow::array::RecordBatch;

const DB_PATH: &str = "../python-duckdb/sales.duckdb";

pub fn query(sql: &str) -> Vec<RecordBatch> {
    let mut driver = ManagedDriver::load_from_name(
        "duckdb",
        None,
        AdbcVersion::default(),
        LOAD_FLAG_DEFAULT,
        None,
    )
    .expect("Failed to load duckdb driver");

    let opts = [(OptionDatabase::Uri, DB_PATH.into())];
    let db = driver.new_database_with_opts(opts).expect("Failed to open database");
    let mut conn = db.new_connection().expect("Failed to create connection");

    let mut stmt = conn.new_statement().expect("Failed to create statement");
    stmt.set_sql_query(sql).expect("Failed to set query");

    let reader = stmt.execute().expect("Failed to execute query");
    reader.map(|r| r.expect("Failed to read batch")).collect()
}
