using System;
using System.Linq;

class Program {
    static int Sieve(int n) {
        bool[] isPrime = new bool[n + 1];
        Array.Fill(isPrime, true);
        isPrime[0] = false;
        isPrime[1] = false;

        for (int p = 2; p * p <= n; p++) {
            if (isPrime[p]) {
                for (int i = p * p; i <= n; i += p) {
                    isPrime[i] = false;
                }
            }
        }

        int count = 0;
        for (int i = 2; i <= n; i++) {
            if (isPrime[i]) count++;
        }
        return count;
    }

    static void Main(string[] args) {
        int n = 1000000;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }

        Console.WriteLine(Sieve(n));
    }
}
