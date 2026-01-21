use std::env;

fn sieve(n: usize) -> i32 {
    let mut primes = vec![true; n + 1];
    let mut p = 2;
    while p * p <= n {
        if primes[p] {
            let mut i = p * p;
            while i <= n {
                primes[i] = false;
                i += p;
            }
        }
        p += 1;
    }
    
    let mut count = 0;
    for p in 2..=n {
        if primes[p] {
            count += 1;
        }
    }
    count
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(1000000)
    } else {
        1000000
    };

    println!("{}", sieve(n));
}
