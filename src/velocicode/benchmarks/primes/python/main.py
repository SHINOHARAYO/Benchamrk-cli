import sys

def sieve(n):
    primes = [True] * (n + 1)
    p = 2
    while (p * p <= n):
        if (primes[p] == True):
            for i in range(p * p, n + 1, p):
                primes[i] = False
        p += 1
    
    # Count primes
    count = 0
    for p in range(2, n + 1):
        if primes[p]:
            count += 1
    return count

if __name__ == "__main__":
    n = 1000000
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    
    print(sieve(n))
