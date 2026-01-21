package main

import (
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strconv"
)

func main() {
	n := 1000000
	if len(os.Args) > 1 {
		if val, err := strconv.Atoi(os.Args[1]); err == nil {
			n = val
		}
	}

	data := make([]int, n)
	for i := 0; i < n; i++ {
		data[i] = rand.Intn(1000000)
	}

	sort.Ints(data)
	fmt.Println(data[0])
}
