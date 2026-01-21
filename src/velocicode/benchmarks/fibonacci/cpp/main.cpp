#include <iostream>
#include <cstdlib>

int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char* argv[]) {
    int n = 35;
    if (argc > 1) {
        n = std::atoi(argv[1]);
    }
    std::cout << fib(n) << std::endl;
    return 0;
}
