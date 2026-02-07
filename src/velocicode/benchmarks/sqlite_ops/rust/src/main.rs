use rusqlite::{params, Connection};
use std::fs;
use std::path::Path;

fn main() -> rusqlite::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = if args.len() > 1 {
        args[1].parse().unwrap_or(10000)
    } else {
        10000
    };

    let db_path = "bench.db";
    if Path::new(db_path).exists() {
        fs::remove_file(db_path).unwrap();
    }

    let conn = Connection::open(db_path)?;

    conn.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)",
        [],
    )?;

    {
        let mut stmt = conn.prepare("INSERT INTO test (value) VALUES (?)")?;
        let mut tx = conn.unchecked_transaction()?; // Using unchecked for speed/simplicity or regular transaction?
        // rusqlite transaction is a bit different.
        // It's better to use conn.transaction() but then we need to move tx.
    }
    // Re-structure transaction usage
    
    let mut tx = conn.unchecked_transaction()?;
    {
        let mut stmt = tx.prepare("INSERT INTO test (value) VALUES (?)")?;
        for i in 0..n {
            stmt.execute(params![format!("value-{}", i)])?;
        }
    }
    tx.commit()?;

    let mut stmt = conn.prepare("SELECT * FROM test")?;
    let mut rows = stmt.query([])?;

    let mut count = 0;
    while let Some(_) = rows.next()? {
        count += 1;
    }

    // drop conn or explicit close not needed in Rust (RAII)
    // But to delete file we should close connection first.
    drop(stmt);
    drop(conn);

    if Path::new(db_path).exists() {
        fs::remove_file(db_path).unwrap();
    }

    Ok(())
}
