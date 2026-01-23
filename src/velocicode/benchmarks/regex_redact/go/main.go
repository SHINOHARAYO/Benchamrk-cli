package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strconv"
	"time"
)

func main() {
	n := 1
	if len(os.Args) > 1 {
		val, err := strconv.Atoi(os.Args[1])
		if err == nil {
			n = val
		}
	}

	_, filename, _, _ := runtime.Caller(0)
	baseDir := filepath.Dir(filepath.Dir(filename))
	dataPath := filepath.Join(baseDir, "data.txt")
    
    if _, err := os.Stat(dataPath); os.IsNotExist(err) {
        dataPath = "data.txt"
        if _, err := os.Stat(dataPath); os.IsNotExist(err) {
             dataPath = "../data.txt"
        }
    }

	contentBytes, err := ioutil.ReadFile(dataPath)
	if err != nil {
		fmt.Printf("Error: data.txt not found\n")
		os.Exit(1)
	}
    
    content := string(contentBytes)

	// Go regexp
	phoneRe := regexp.MustCompile(`\d{3}-\d{3}-\d{4}`)
	emailRe := regexp.MustCompile(`[a-z]{8}@example\.com`)

	start := time.Now()

	var result string
	for i := 0; i < n; i++ {
        // Go strings are immutable. ReplaceAllString returns new string.
		temp := phoneRe.ReplaceAllString(content, "[PHONE]")
		result = emailRe.ReplaceAllString(temp, "[EMAIL]")
	}

	duration := time.Since(start)
	_ = duration

	if len(result) == 0 {
		fmt.Println("Error")
	}
}
