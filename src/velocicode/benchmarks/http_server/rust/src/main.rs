use hyper::{Body, Request, Response, Server, Client};
use hyper::service::{make_service_fn, service_fn};
use std::convert::Infallible;
use std::net::SocketAddr;
use tokio::sync::oneshot;

async fn hello(_: Request<Body>) -> Result<Response<Body>, Infallible> {
    Ok(Response::new(Body::from("Hello World")))
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n = if args.len() > 1 {
        args[1].parse().unwrap_or(5000)
    } else {
        5000
    };

    let addr = SocketAddr::from(([127, 0, 0, 1], 0));

    let make_svc = make_service_fn(|_conn| async {
        Ok::<_, Infallible>(service_fn(hello))
    });

    let server = Server::bind(&addr).serve(make_svc);
    let local_addr = server.local_addr();

    let (tx, rx) = oneshot::channel::<()>();

    let server = server.with_graceful_shutdown(async {
        rx.await.ok();
    });

    tokio::spawn(async move {
        if let Err(e) = server.await {
            eprintln!("server error: {}", e);
        }
    });

    // Client
    let client = Client::new();
    let uri = format!("http://{}", local_addr).parse().unwrap();

    for _ in 0..n {
        let _ = client.get(uri.clone()).await;
        // consume body?
    }

    let _ = tx.send(());
}
