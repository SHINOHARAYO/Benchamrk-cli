use std::env;
use std::iter;
use rand::Rng;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(1000000)
    } else {
        1000000
    };

    let mut rng = rand::thread_rng();
    let mut data: Vec<i32> = (0..n).map(|_| rng.gen_range(0..1000000)).collect();

    data.sort();

    println!("{}", data[0]);
}
