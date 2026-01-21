package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
)

func generateMatrix(n int) [][]float64 {
	m := make([][]float64, n)
	for i := range m {
		m[i] = make([]float64, n)
		for j := range m[i] {
			m[i][j] = rand.Float64()
		}
	}
	return m
}

func matMul(a, b [][]float64, n int) [][]float64 {
	c := make([][]float64, n)
	for i := range c {
		c[i] = make([]float64, n)
		for i := 0; i < n; i++ {
			for k := 0; k < n; k++ {
				for j := 0; j < n; j++ {
					c[i][j] += a[i][k] * b[k][j]
				}
			}
		}
	}
	return c
}

func main() {
	n := 200
	if len(os.Args) > 1 {
		if val, err := strconv.Atoi(os.Args[1]); err == nil {
			n = val
		}
	}

	a := generateMatrix(n)
	b := generateMatrix(n)
	c := matMul(a, b, n)
	fmt.Println(c[0][0])
}
