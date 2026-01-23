import re
import sys
import time
import os

def main():
    n = 1
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            pass

    # data.txt in ../data.txt
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data.txt")
    
    if not os.path.exists(data_path):
        data_path = "data.txt" # fallback
        if not os.path.exists(data_path):
             print("Error: data.txt not found")
             sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pre-compile regex for fairness?
    # Yes, typically we benchmark RE execution not compilation if we are looping
    
    # Phone: XXX-XXX-XXXX
    # Email: [a-z]{8}@example.com
    # Basic patterns to match generator
    phone_re = re.compile(r'\d{3}-\d{3}-\d{4}')
    email_re = re.compile(r'[a-z]{8}@example\.com')

    start_time = time.time()
    
    for _ in range(n):
        # We need to act on the content.
        # String is immutable, so replace returns new string.
        # In loop, we should probably operate on original content each time?
        # Yes, otherwise we replace replacemnts.
        
        temp = phone_re.sub("[PHONE]", content)
        result = email_re.sub("[EMAIL]", temp)
        
    duration = time.time() - start_time
    
    if len(result) == 0:
        print("Error")

if __name__ == "__main__":
    main()
