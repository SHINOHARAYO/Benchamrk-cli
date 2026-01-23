const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 1;

// Path to data.json
let dataPath = path.join(__dirname, '..', 'data.json');

try {
    if (!fs.existsSync(dataPath)) {
        if (fs.existsSync('data.json')) {
            dataPath = 'data.json';
        } else {
            console.log("Error: data.json not found");
            process.exit(1);
        }
    }

    const jsonStr = fs.readFileSync(dataPath, 'utf8');

    const start = process.hrtime();

    let data;
    for (let i = 0; i < n; i++) {
        data = JSON.parse(jsonStr);
    }

    const diff = process.hrtime(start);
    const duration = diff[0] + diff[1] / 1e9; // seconds

    if (!data || data.length === 0) {
        console.log("Error");
    }

} catch (e) {
    console.error(e);
    process.exit(1);
}
