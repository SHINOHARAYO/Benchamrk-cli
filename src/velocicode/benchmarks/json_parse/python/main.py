import json
import sys
import time
import os

def main():
    # Iterations usually 1 for this, or small, as parsing 12MB is slow
    n = 1
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            pass

    # Locale data path
    # Assuming script is run from .../python/
    # data.json is in .../json_parse/data.json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data.json")
    
    if not os.path.exists(data_path):
        # Fallback to current dir if copied
        data_path = "data.json"
        
    if not os.path.exists(data_path):
        print("Error: data.json not found")
        sys.exit(1)

    # Read file into memory string first to benchmark PARSING, not I/O
    with open(data_path, "r") as f:
        json_str = f.read()

    start_time = time.time()
    
    for _ in range(n):
        data = json.loads(json_str)
        
    duration = time.time() - start_time
    
    # Prevent optimization
    if len(data) == 0:
        print("Error")

if __name__ == "__main__":
    main()
