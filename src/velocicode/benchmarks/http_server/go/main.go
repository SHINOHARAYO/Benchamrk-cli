package main

import (
    "fmt"
    "io"
    "net"
    "net/http"
    "os"
    "strconv"
    "sync"
    "time"
)

func handler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/plain")
    w.Header().Set("Content-Length", "11")
    fmt.Fprint(w, "Hello World")
}

func runClient(url string, n int) {
    client := &http.Client{
        Transport: &http.Transport{
            MaxIdleConnsPerHost: 100, // Keep-alive
        },
    }

    for i := 0; i < n; i++ {
        resp, err := client.Get(url)
        if err != nil {
            fmt.Println("Error:", err)
            continue
        }
        io.Copy(io.Discard, resp.Body)
        resp.Body.Close()
    }
}

func main() {
    n := 5000
    if len(os.Args) > 1 {
        if val, err := strconv.Atoi(os.Args[1]); err == nil {
            n = val
        }
    }

    listener, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        panic(err)
    }
    port := listener.Addr().(*net.TCPAddr).Port
    url := fmt.Sprintf("http://127.0.0.1:%d/", port)

    var wg sync.WaitGroup
    wg.Add(1)

    go func() {
        http.Serve(listener, http.HandlerFunc(handler))
        wg.Done()
    }()

    // Give server a moment? No need, Listen creates socket.
    
    start := time.Now()
    runClient(url, n)
    elapsed := time.Since(start)
    _ = elapsed

    // Close server?
    listener.Close()
    // wg.Wait() // Don't wait, just exit
    
    // fmt.Printf("Time: %s\n", elapsed)
}
