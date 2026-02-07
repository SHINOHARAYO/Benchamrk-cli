using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        int n = 5000;
        if (args.Length > 0)
        {
            int.TryParse(args[0], out n);
        }

        // Use random port
        var listener = new HttpListener();
        
        int port = GetFreePort();
        string url = $"http://127.0.0.1:{port}/";
        listener.Prefixes.Add(url);
        
        listener.Start();
        
        var serverTask = Task.Run(async () =>
        {
            try {
                while (listener.IsListening)
                {
                    var ctx = await listener.GetContextAsync();
                    var resp = ctx.Response;
                    resp.ContentType = "text/plain";
                    resp.ContentLength64 = 11;
                    byte[] buffer = System.Text.Encoding.UTF8.GetBytes("Hello World");
                    resp.OutputStream.Write(buffer, 0, buffer.Length);
                    resp.OutputStream.Close();
                }
            } catch {}
        });

        using (var client = new HttpClient())
        {
            for (int i = 0; i < n; i++)
            {
                var response = await client.GetAsync(url);
                response.EnsureSuccessStatusCode();
            }
        }
        
        listener.Stop();
        // await serverTask; // Will throw on stop
    }

    static int GetFreePort()
    {
        var listener = new System.Net.Sockets.TcpListener(IPAddress.Loopback, 0);
        listener.Start();
        int port = ((IPEndPoint)listener.LocalEndpoint).Port;
        listener.Stop();
        return port;
    }
}
