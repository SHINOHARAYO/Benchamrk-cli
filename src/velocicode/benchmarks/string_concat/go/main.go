package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: main <iterations>")
		os.Exit(1)
	}

	n := 1000000
	if len(os.Args) > 1 {
		val, err := strconv.Atoi(os.Args[1])
		if err == nil {
			n = val
		}
	}

	s := "velocicode"
	var builder strings.Builder
	
	// Similar to C++, we won't pre-grow (Grow) to test dynamic allocation policies.
	
	for i := 0; i < n; i++ {
		builder.WriteString(s)
	}

	result := builder.String()

	// Prevent optimization
	if len(result) == 0 {
		fmt.Println("Error")
	}
}
