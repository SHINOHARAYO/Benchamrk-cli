use std::fs;
use std::env;
use std::path::Path;
use serde_json::Value;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(1)
    } else {
        1
    };

    // Locate data.json
    let mut data_path = Path::new("../../data.json");
    if !data_path.exists() {
        data_path = Path::new("data.json");
        if !data_path.exists() {
             data_path = Path::new("../data.json");
        }
    }

    let json_str = match fs::read_to_string(data_path) {
        Ok(c) => c,
        Err(_) => {
            eprintln!("Error: data.json not found at {:?}", data_path);
            std::process::exit(1);
        }
    };

    let mut result_array_len = 0;

    for _ in 0..n {
        let v: Value = serde_json::from_str(&json_str).expect("Invalid JSON");
        // Accessing data to ensure parsing actually happened
        if let Some(arr) = v.as_array() {
            result_array_len = arr.len();
        }
    }

    if result_array_len == 0 {
        // Just a check to prevent optimization
        // (Though with side effects like printing or complex logic, dynamic dispatch etc. 
        // usually safe, but good to check)
       // println!("Warning: Empty JSON result");
    }
}
