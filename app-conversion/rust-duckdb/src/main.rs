mod db;

use arrow::util::pretty::print_batches;

fn main() {
    let batches = db::query("SELECT * FROM sales");
    print_batches(&batches).expect("Failed to print");
}
