const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 1000000;

const s = "velocicode";
const parts = [];

for (let i = 0; i < n; i++) {
    parts.push(s);
}

const result = parts.join('');

if (result.length === 0) {
    console.log("Error");
}
