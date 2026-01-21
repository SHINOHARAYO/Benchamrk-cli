#include <iostream>
#include <vector>
#include <cstdlib>

using namespace std;

int sieve(int n) {
    vector<bool> primes(n + 1, true);
    for (int p = 2; p * p <= n; p++) {
        if (primes[p] == true) {
            for (int i = p * p; i <= n; i += p)
                primes[i] = false;
        }
    }
    
    int count = 0;
    for (int p = 2; p <= n; p++)
        if (primes[p]) count++;
    return count;
}

int main(int argc, char* argv[]) {
    int n = 1000000;
    if (argc > 1) n = atoi(argv[1]);

    cout << sieve(n) << endl;
    return 0;
}
