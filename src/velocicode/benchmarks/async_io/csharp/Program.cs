using System;
using System.Collections.Generic;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        int n = 10000;
        if (args.Length > 0)
        {
            int.TryParse(args[0], out n);
        }

        int duration = 10; // 10ms
        var tasks = new List<Task>(n);

        for (int i = 0; i < n; i++)
        {
            tasks.Add(IoTask(duration));
        }

        await Task.WhenAll(tasks);
    }

    static async Task IoTask(int duration)
    {
        await Task.Delay(duration);
    }
}
