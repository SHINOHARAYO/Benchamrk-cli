use std::fs;
use std::env;
use std::path::Path;
use regex::Regex;
use std::borrow::Cow;

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(1)
    } else {
        1
    };

    // Locate data.txt
    // Assuming binary runs in source/rust or source/rust/target/release
    // We need to look up relative to the project root or source file location.
    // runner.py sets cwd to 'src/velocicode/benchmarks/regex_redact/rust'
    let mut data_path = Path::new("../../data.txt");
    if !data_path.exists() {
        data_path = Path::new("data.txt");
        if !data_path.exists() {
            // Check one level up if in nested dir
            data_path = Path::new("../data.txt");
        }
    }

    let content = match fs::read_to_string(data_path) {
        Ok(c) => c,
        Err(_) => {
            eprintln!("Error: data.txt not found at {:?}", data_path);
            std::process::exit(1);
        }
    };

    let phone_re = Regex::new(r"\d{3}-\d{3}-\d{4}").unwrap();
    let email_re = Regex::new(r"[a-z]{8}@example\.com").unwrap();

    let mut result_len = 0;

    for _ in 0..n {
        let temp = phone_re.replace_all(&content, "[PHONE]");
        // temp is Cow<str>. result needs to be owned or Cow?
        // replace_all returns Cow.
        let result = email_re.replace_all(&temp, "[EMAIL]");
        result_len = result.len();
    }

    if result_len == 0 {
        println!("Error");
    }
}
