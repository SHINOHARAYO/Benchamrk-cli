use std::env;
use std::time::Duration;
use tokio::time::sleep;

async def io_task(duration: u64) {
    sleep(Duration::from_millis(duration)).await;
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    let mut n = 10000;
    if args.len() > 1 {
        if let Ok(val) = args[1].parse() {
            n = val;
        }
    }

    let duration = 10; // 10ms

    let mut handles = Vec::with_capacity(n);

    for _ in 0..n {
        handles.push(tokio::spawn(async move {
            sleep(Duration::from_millis(duration)).await;
        }));
    }

    for handle in handles {
        let _ = handle.await;
    }
}
