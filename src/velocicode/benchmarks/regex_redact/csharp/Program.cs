using System;
using System.IO;
using System.Text.RegularExpressions;

class Program {
    static void Main(string[] args) {
        int n = 1;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }

        string baseDir = AppDomain.CurrentDomain.BaseDirectory;
        string dataPath = Path.GetFullPath(Path.Combine(baseDir, "../../../data.txt"));
        
        if (!File.Exists(dataPath)) {
             dataPath = "data.txt";
             if (!File.Exists(dataPath)) {
                 dataPath = "../data.txt";
             }
        }

        if (!File.Exists(dataPath)) {
            Console.WriteLine("Error: data.txt not found");
            return;
        }

        string content = File.ReadAllText(dataPath);

        // Compiled Regex for performance equal to others
        Regex phoneRe = new Regex(@"\d{3}-\d{3}-\d{4}", RegexOptions.Compiled);
        Regex emailRe = new Regex(@"[a-z]{8}@example\.com", RegexOptions.Compiled);

        var start = DateTime.Now;

        string result = "";
        for (int i = 0; i < n; i++) {
            string temp = phoneRe.Replace(content, "[PHONE]");
            result = emailRe.Replace(temp, "[EMAIL]");
        }

        var duration = DateTime.Now - start;

        if (result.Length == 0) {
            Console.WriteLine("Error");
        }
    }
}
