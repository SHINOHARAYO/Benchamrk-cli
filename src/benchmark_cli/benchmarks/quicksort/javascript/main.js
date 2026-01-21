const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 1000000;

const data = new Int32Array(n);
for (let i = 0; i < n; i++) {
    data[i] = Math.floor(Math.random() * 1000000);
}

data.sort();

console.log(data[0]);
