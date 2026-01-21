use std::env;

fn fib(n: u32) -> u32 {
    if n <= 1 {
        return n;
    }
    fib(n - 1) + fib(n - 2)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(35)
    } else {
        35
    };
    println!("{}", fib(n));
}
