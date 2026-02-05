import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

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

        // Locate data.json
        Path dataPath = Paths.get("../../data.json");
        if (!Files.exists(dataPath)) {
            dataPath = Paths.get("data.json");
            if (!Files.exists(dataPath)) {
                dataPath = Paths.get("../data.json");
            }
        }

        if (!Files.exists(dataPath)) {
            System.err.println("Error: data.json not found");
            System.exit(1);
        }

        try {
            // Read all bytes to memory first
            String jsonStr = Files.readString(dataPath);
            ObjectMapper mapper = new ObjectMapper();
            
            for (int i = 0; i < n; i++) {
                JsonNode root = mapper.readTree(jsonStr);
                // Prevent optimization
                if (root.isArray()) {
                    int size = root.size();
                    if (size < 0) System.out.println("Impossible");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
