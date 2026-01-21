import java.util.Arrays;

public class Main {
    static int sieve(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
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
            if (isPrime[i])
                count++;
        }
        return count;
    }

    public static void main(String[] args) {
        int n = 1000000;
        if (args.length > 0) {
            try {
                n = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                n = 1000000;
            }
        }

        System.out.println(sieve(n));
    }
}
