using System;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;

class Program {
    static void Main(string[] args) {
        int n = 1;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }

        // Locate data.json
        // .../csharp/Program.cs -> .../json_parse/data.json
        string baseDir = AppDomain.CurrentDomain.BaseDirectory;
        // Search up until we find json_parse or data.json
        string dataPath = Path.GetFullPath(Path.Combine(baseDir, "../../../data.json"));
        
        if (!File.Exists(dataPath)) {
             // Fallback
             dataPath = "data.json";
             if (!File.Exists(dataPath)) {
                 dataPath = "../data.json";
             }
        }

        if (!File.Exists(dataPath)) {
            Console.WriteLine("Error: data.json not found");
            return;
        }

        string jsonStr = File.ReadAllText(dataPath);

        var start = DateTime.Now;

        List<Dictionary<string, object>>? data = null;

        for (int i = 0; i < n; i++) {
             // Deserialize to generic structure
             // System.Text.Json uses JsonElement for "object", not Dictionary<string, object> by default for generic.
             // To be fair to Python/JS which return Dict/Object, we should parse to JsonElement or similar node tree.
             // JsonDocument.Parse is faster but produces disposable doc.
             // JsonSerializer.Deserialize<object> produces JsonElement.
             
             data = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(jsonStr);
        }

        var duration = DateTime.Now - start;

        if (data == null || data.Count == 0) {
            Console.WriteLine("Error");
        }
    }
}
