import sys
import random
import time

sys.setrecursionlimit(2000000)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

if __name__ == "__main__":
    n = 1000000
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    
    # Generate random data
    data = [random.randint(0, 1000000) for _ in range(n)]
    
    sorted_data = quick_sort(data)
    # Print first element to prevent optimization
    print(sorted_data[0])
