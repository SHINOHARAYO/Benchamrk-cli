import java.util.Random;

public class Main {
    static double[][] generateMatrix(int n) {
        double[][] m = new double[n][n];
        Random rand = new Random(42);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                m[i][j] = rand.nextDouble();
            }
        }
        return m;
    }

    static double[][] matMul(double[][] a, double[][] b, int n) {
        double[][] c = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                for (int j = 0; j < n; j++) {
                    c[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return c;
    }

    public static void main(String[] args) {
        int n = 200;
        if (args.length > 0) {
            try {
                n = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                n = 200;
            }
        }

        double[][] a = generateMatrix(n);
        double[][] b = generateMatrix(n);
        double[][] c = matMul(a, b, n);

        System.out.println(c[0][0]);
    }
}
