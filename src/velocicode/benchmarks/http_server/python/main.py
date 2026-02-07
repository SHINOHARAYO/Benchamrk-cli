import http.server
import socketserver
import threading
import time
import http.client
import sys

PORT = 0 # Let OS pick port
Handler = http.server.BaseHTTPRequestHandler

class FastHandler(Handler):
    def log_message(self, format, *args):
        pass # Silence logging
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", "11")
        self.end_headers()
        self.wfile.write(b"Hello World")

def run_server(server_ready_event, server_socket_info):
    # Create server
    with socketserver.TCPServer(("127.0.0.1", 0), FastHandler) as httpd:
        server_socket_info['port'] = httpd.server_address[1]
        server_ready_event.set()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        except OSError: # Socket closed
            pass

def run_client(port, n):
    conn = http.client.HTTPConnection("127.0.0.1", port)
    for _ in range(n):
        conn.request("GET", "/")
        resp = conn.getresponse()
        resp.read() # Consume
    conn.close()

def main():
    n = 5000 # Default requests
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except:
            pass
            
    server_ready = threading.Event()
    server_info = {}
    
    server_thread = threading.Thread(target=run_server, args=(server_ready, server_info))
    server_thread.daemon = True
    server_thread.start()
    
    server_ready.wait()
    port = server_info['port']
    
    # Warmup? Maybe.
    
    start = time.time()
    run_client(port, n)
    end = time.time()
    
    duration = end - start
    # print(f"Requests per second: {n / duration:.2f}")

if __name__ == "__main__":
    main()
