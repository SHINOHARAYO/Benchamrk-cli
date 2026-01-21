use std::env;

fn generate_matrix(n: usize) -> Vec<Vec<f64>> {
    let mut m = vec![vec![0.0; n]; n];
    for i in 0..n {
        for j in 0..n {
            m[i][j] = (i as f64 + j as f64) * 0.001; // Simple deterministic generation
        }
    }
    m
}

fn mat_mul(a: &Vec<Vec<f64>>, b: &Vec<Vec<f64>>, n: usize) -> Vec<Vec<f64>> {
    let mut c = vec![vec![0.0; n]; n];
    for i in 0..n {
        for k in 0..n {
            for j in 0..n {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    c
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(200)
    } else {
        200
    };

    let a = generate_matrix(n);
    let b = generate_matrix(n);
    let c = mat_mul(&a, &b, n);
    println!("{}", c[0][0]);
}
