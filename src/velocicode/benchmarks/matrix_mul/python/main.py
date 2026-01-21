import sys
import random

def generate_matrix(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]

def mat_mul(A, B, n):
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sum_val = 0
            for k in range(n):
                sum_val += A[i][k] * B[k][j]
            C[i][j] = sum_val
    return C

if __name__ == "__main__":
    n = 200
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    
    A = generate_matrix(n)
    B = generate_matrix(n)
    C = mat_mul(A, B, n)
    print(C[0][0]) # prevent optimization
