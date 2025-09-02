import http.server
import socketserver
import threading
import webbrowser
import time

def run_server():
    PORT = 5000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
print("Starting test server and opening browser...")
# Give server a moment to start
time.sleep(1)
# Try to open browser automatically
webbrowser.open('http://localhost:5000')
print("Press Ctrl+C to stop the test server")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Test server stopped")
