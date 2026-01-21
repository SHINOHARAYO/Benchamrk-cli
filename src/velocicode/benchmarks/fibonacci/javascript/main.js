function fib(n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 35;

console.log(fib(n));
