import sys
import time

def main():
    n = 1000000
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            pass

    # Adjust N for string concat as it can be memory heavy
    # If the runner sends small N (e.g. 100), we probably want to scale it up 
    # internally to make the benchmark measurable, OR assume the runner N is 
    # the NUMBER OF STRINGS to concat.
    # Velocicode runner usually treats N as "number of times to run the whole benchmark".
    # BUT for these algorithm benchmarks, N usually means "input size". 
    # Let's check how other benchmarks handle it.
    # Fibonacci: N is the Nth number (e.g. 40).
    # Matrix Mul: N is matrix size (e.g. 512).
    # Primes: N is limit (e.g. 1000000).
    
    # So for String Concat, N should be "Number of concats".
    # Let's default a high number for meaningful work if N is small?
    # No, the runner config usually specifies the input size. 
    # Let's look at config.yaml later. For now, assume arg is N.
    
    parts = []
    s = "velocicode"
    
    start_time = time.time()
    
    for _ in range(n):
        parts.append(s)
        
    result = "".join(parts)
    
    duration = time.time() - start_time
    
    # Prevent optimization
    if len(result) == 0:
        print("Error")

if __name__ == "__main__":
    main()
