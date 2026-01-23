import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Main {
    public static void main(String[] args) {
        int n = 1;
        if (args.length > 0) {
            try {
                n = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                // ignore
            }
        }

        Path dataPath = Paths.get("data.txt");
        if (!Files.exists(dataPath)) {
            dataPath = Paths.get("..", "data.txt");
            if (!Files.exists(dataPath)) {
                System.out.println("Error: data.txt not found");
                return;
            }
        }

        String content = "";
        try {
            content = Files.readString(dataPath);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        Pattern phoneRe = Pattern.compile("\\d{3}-\\d{3}-\\d{4}");
        Pattern emailRe = Pattern.compile("[a-z]{8}@example\\.com");

        String result = "";

        for (int i = 0; i < n; i++) {
            // Java Matcher.replaceAll()
            Matcher phoneMatcher = phoneRe.matcher(content);
            String temp = phoneMatcher.replaceAll("[PHONE]");

            Matcher emailMatcher = emailRe.matcher(temp);
            result = emailMatcher.replaceAll("[EMAIL]");
        }

        if (result.length() == 0) {
            System.out.println("Error");
        }
    }
}
