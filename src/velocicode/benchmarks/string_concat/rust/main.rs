use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n: i32 = if args.len() > 1 {
        args[1].parse().unwrap_or(1000000)
    } else {
        1000000
    };

    let s = "velocicode";
    let mut result = String::new();
    
    // Again, no capacity reservation to test reallocation speed
    for _ in 0..n {
        result.push_str(s);
    }

    // Prevent optimization
    if result.len() == 0 {
        println!("Error");
    }
}
