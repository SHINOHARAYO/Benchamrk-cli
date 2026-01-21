import java.util.Arrays;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        int n = 1000000;
        if (args.length > 0) {
            try {
                n = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                n = 1000000;
            }
        }

        int[] data = new int[n];
        Random rand = new Random(42);
        for (int i = 0; i < n; i++) {
            data[i] = rand.nextInt(1000000);
        }

        Arrays.sort(data);

        System.out.println(data[0]);
    }
}
