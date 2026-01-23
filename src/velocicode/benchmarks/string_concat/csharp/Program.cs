using System;
using System.Text;

class Program {
    static void Main(string[] args) {
        int n = 1000000;
        if (args.Length > 0) {
            int.TryParse(args[0], out n);
        }

        string s = "velocicode";
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < n; i++) {
            sb.Append(s);
        }

        string result = sb.ToString();

        if (result.Length == 0) {
            Console.WriteLine("Error");
        }
    }
}
