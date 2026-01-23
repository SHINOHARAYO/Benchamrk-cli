
public class Main {
    public static void main(String[] args) {
        int n = 1000000;
        if (args.length > 0) {
            try {
                n = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                // ignore
            }
        }

        String s = "velocicode";
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < n; i++) {
            sb.append(s);
        }

        String result = sb.toString();

        if (result.length() == 0) {
            System.out.println("Error");
        }
    }
}
