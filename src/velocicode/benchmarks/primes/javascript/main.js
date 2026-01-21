function sieve(n) {
    const primes = new Uint8Array(n + 1).fill(1);

    for (let p = 2; p * p <= n; p++) {
        if (primes[p] === 1) {
            for (let i = p * p; i <= n; i += p)
                primes[i] = 0;
        }
    }

    let count = 0;
    for (let p = 2; p <= n; p++)
        if (primes[p] === 1) count++;
    return count;
}

const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 1000000;

console.log(sieve(n));
