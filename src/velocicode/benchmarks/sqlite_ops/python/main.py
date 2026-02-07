import sqlite3
import sys
import time
import os

def main():
    n = 10000 # inserts
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except:
            pass

    db_path = "bench.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    # Optimization: synchronous=OFF drastically improves insert speed by reducing fsyncs
    # However, for benchmark we might want default safety?
    # Usually "System & I/O" benchmarks want to test I/O.
    # If we disable sync, it becomes CPU/Memory buffer test until flush.
    # Let's keep defaults but wrap inserts in ONE transaction.
    
    conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    
    start = time.time()
    
    # 1. Inserts
    # Wrapped in transaction
    conn.execute("BEGIN TRANSACTION")
    for i in range(n):
        conn.execute("INSERT INTO test (value) VALUES (?)", (f"value-{i}",))
    conn.execute("COMMIT")
    
    # 2. Selects
    # Select all or random? sequential?
    # Listing said "Select 10,000 records".
    # Iterate cursor.
    cursor = conn.execute("SELECT * FROM test")
    count = 0
    for row in cursor:
        count += 1
        
    end = time.time()
    conn.close()
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
        
    if count != n:
        print(f"Error: expected {n} rows, got {count}")

if __name__ == "__main__":
    main()
