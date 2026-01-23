package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
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

	// Locate data.json
	// .../go/main.go -> .../json_parse/data.json
	
	// Get current file path hack for dev, or use relative
	_, filename, _, _ := runtime.Caller(0)
	baseDir := filepath.Dir(filepath.Dir(filename))
	dataPath := filepath.Join(baseDir, "data.json")
    
    // Fallback if running compiled binary from elsewhere
    if _, err := os.Stat(dataPath); os.IsNotExist(err) {
        dataPath = "data.json"
        
        // Try parent dir if running from bin/
        if _, err := os.Stat(dataPath); os.IsNotExist(err) {
             dataPath = "../data.json"
        }
    }

	content, err := ioutil.ReadFile(dataPath)
	if err != nil {
		fmt.Printf("Error: data.json not found at %s\n", dataPath)
		os.Exit(1)
	}
	
	// Convert to string to match other langs? 
	// Go json.Unmarshal takes []byte, which is better.
	// We'll use []byte as it's idiomatic in Go.

	start := time.Now()

	var data []map[string]interface{}
	
	for i := 0; i < n; i++ {
		// Reset slices/maps? No, unmarshal allocates new unless we reuse.
		// For fair "Parsing" benchmark, we should allocate new.
		data = nil 
		err = json.Unmarshal(content, &data)
		if err != nil {
			fmt.Println("Error parsing:", err)
			os.Exit(1)
		}
	}

	duration := time.Since(start)
	_ = duration

	if len(data) == 0 {
		fmt.Println("Error")
	}
}
