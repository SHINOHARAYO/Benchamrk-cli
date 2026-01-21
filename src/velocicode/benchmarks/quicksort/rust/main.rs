use std::env;
use std::iter;
struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Self {
        Lcg { state: seed }
    }

    fn next(&mut self) -> u32 {
        // Linear Congruential Generator config (same as glibc's rand)
        self.state = (self.state.wrapping_mul(1103515245).wrapping_add(12345)) % 2147483648;
        self.state as u32
    }
    
    fn gen_range(&mut self, range: std::ops::Range<i32>) -> i32 {
        let min = range.start;
        let max = range.end;
        let width = (max - min) as u32;
        (self.next() % width) as i32 + min
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(1000000)
    } else {
        1000000
    };

    let mut rng = Lcg::new(12345);
    let mut data: Vec<i32> = (0..n).map(|_| rng.gen_range(0..1000000)).collect();

    data.sort();

    println!("{}", data[0]);
}
