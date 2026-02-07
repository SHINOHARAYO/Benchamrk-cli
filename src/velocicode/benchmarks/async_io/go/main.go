package main

import (
    "os"
    "strconv"
    "sync"
    "time"
)

func ioTask(duration time.Duration, wg *sync.WaitGroup) {
    defer wg.Done()
    time.Sleep(duration)
}

func main() {
    n := 10000
    if len(os.Args) > 1 {
        if val, err := strconv.Atoi(os.Args[1]); err == nil {
            n = val
        }
    }

    var wg sync.WaitGroup
    duration := 10 * time.Millisecond

    for i := 0; i < n; i++ {
        wg.Add(1)
        go ioTask(duration, &wg)
    }

    wg.Wait()
}
