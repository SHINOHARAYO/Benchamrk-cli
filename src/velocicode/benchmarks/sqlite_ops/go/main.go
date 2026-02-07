package main

import (
    "database/sql"
    "fmt"
    "os"
    "strconv"

    _ "github.com/mattn/go-sqlite3"
)

func main() {
    n := 10000
    if len(os.Args) > 1 {
        if val, err := strconv.Atoi(os.Args[1]); err == nil {
            n = val
        }
    }

    dbPath := "bench.db"
    os.Remove(dbPath)

    db, err := sql.Open("sqlite3", dbPath)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    _, err = db.Exec("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    if err != nil {
        panic(err)
    }

    tx, err := db.Begin()
    if err != nil {
        panic(err)
    }

    stmt, err := tx.Prepare("INSERT INTO test (value) VALUES (?)")
    if err != nil {
        panic(err)
    }
    defer stmt.Close()

    for i := 0; i < n; i++ {
        _, err = stmt.Exec(fmt.Sprintf("value-%d", i))
        if err != nil {
            panic(err)
        }
    }

    err = tx.Commit()
    if err != nil {
        panic(err)
    }

    rows, err := db.Query("SELECT * FROM test")
    if err != nil {
        panic(err)
    }
    count := 0
    for rows.Next() {
        count++
    }
    rows.Close()

    os.Remove(dbPath)
}
