package main

import (
	"fmt"
	"os"
	"strconv"
)

func sieve(n int) int {
	primes := make([]bool, n+1)
	for i := 0; i <= n; i++ {
		primes[i] = true
	}

	for p := 2; p*p <= n; p++ {
		if primes[p] == true {
			for i := p * p; i <= n; i += p {
				primes[i] = false
			}
		}
	}

	count := 0
	for p := 2; p <= n; p++ {
		if primes[p] {
			count++
		}
	}
	return count
}

func main() {
	n := 1000000
	if len(os.Args) > 1 {
		if val, err := strconv.Atoi(os.Args[1]); err == nil {
			n = val
		}
	}
	fmt.Println(sieve(n))
}
