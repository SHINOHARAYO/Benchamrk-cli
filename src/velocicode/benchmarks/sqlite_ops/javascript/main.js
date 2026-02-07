const Database = require('better-sqlite3');
const fs = require('fs');

const dbPath = 'bench.db';
if (fs.existsSync(dbPath)) {
    fs.unlinkSync(dbPath);
}

const db = new Database(dbPath);

let n = 10000;
if (process.argv.length > 2) {
    n = parseInt(process.argv[2]);
}

db.exec("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)");

// 1. Insert
const insert = db.prepare('INSERT INTO test (value) VALUES (?)');

const insertMany = db.transaction((count) => {
    for (let i = 0; i < count; i++) {
        insert.run(`value-${i}`);
    }
});

insertMany(n);

// 2. Select
const select = db.prepare('SELECT * FROM test');
let count = 0;
for (const row of select.iterate()) {
    count++;
}

db.close();

if (fs.existsSync(dbPath)) {
    fs.unlinkSync(dbPath);
}
