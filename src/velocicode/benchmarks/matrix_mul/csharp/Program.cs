using System;

class Program {
    static double[][] GenerateMatrix(int n) {
        double[][] m = new double[n][];
        Random rand = new Random(42);
        for (int i = 0; i < n; i++) {
            m[i] = new double[n];
            for (int j = 0; j < n; j++) {
                m[i][j] = rand.NextDouble();
            }
        }
        return m;
    }

    static double[][] MatMul(double[][] a, double[][] b, int n) {
        double[][] c = new double[n][];
        for (int i = 0; i < n; i++) {
            c[i] = new double[n];
        }

        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                for (int j = 0; j < n; j++) {
                    c[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return c;
    }

    static void Main(string[] args) {
        int n = 200;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }

        double[][] a = GenerateMatrix(n);
        double[][] b = GenerateMatrix(n);
        double[][] c = MatMul(a, b, n);

        Console.WriteLine(c[0][0]);
    }
}
