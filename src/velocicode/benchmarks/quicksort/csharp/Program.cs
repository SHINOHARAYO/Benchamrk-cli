using System;

class Program {
    static void Main(string[] args) {
        int n = 1000000;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }

        int[] data = new int[n];
        Random rand = new Random(42);
        for (int i = 0; i < n; i++) {
            data[i] = rand.Next(0, 1000000);
        }

        Array.Sort(data);

        Console.WriteLine(data[0]);
    }
}
