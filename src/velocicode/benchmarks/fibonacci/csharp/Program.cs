using System;

class Program {
    static int Fib(int n) {
        if (n <= 1) return n;
        return Fib(n - 1) + Fib(n - 2);
    }

    static void Main(string[] args) {
        int n = 40;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }
        Console.WriteLine(Fib(n));
    }
}
