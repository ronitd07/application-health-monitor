import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            response = {"status": "health"}

        elif self.path == "/version":
            status = 200
            response = {"version": "1.0.0"}

        else:
            status = 404
            response = {"error": "Not found"}

        body = json.dumps(response).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Server running at http://127.0.0.1:8000")
    server.serve_forever()
