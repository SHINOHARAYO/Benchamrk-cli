const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 1;

let dataPath = path.join(__dirname, '..', 'data.txt');

try {
    if (!fs.existsSync(dataPath)) {
        dataPath = 'data.txt';
        if (!fs.existsSync(dataPath)) {
            console.log("Error: data.txt not found");
            process.exit(1);
        }
    }

    const content = fs.readFileSync(dataPath, 'utf8');

    // JS RegExp are objects.
    // 'g' flag is needed for global replacement
    const phoneRe = /\d{3}-\d{3}-\d{4}/g;
    const emailRe = /[a-z]{8}@example\.com/g;

    const start = process.hrtime();

    let result = '';
    for (let i = 0; i < n; i++) {
        let temp = content.replace(phoneRe, "[PHONE]");
        result = temp.replace(emailRe, "[EMAIL]");
    }

    const diff = process.hrtime(start);
    const duration = diff[0] + diff[1] / 1e9;

    if (result.length === 0) {
        console.log("Error");
    }

} catch (e) {
    console.error(e);
    process.exit(1);
}
