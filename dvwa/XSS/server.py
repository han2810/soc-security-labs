from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class MyHandler(BaseHTTPRequestHandler):

    def add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.add_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.add_cors_headers()
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

        self.wfile.write("Python server đang chạy".encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))

        body = self.rfile.read(content_length).decode("utf-8")

        print("Raw body:", body)

        try:
            data = json.loads(body)
            print("Dữ liệu JSON nhận được:", data)

            response_data = {
                "status": "success",
                "message": "Server đã nhận dữ liệu",
                "received": data,
            }

            response_body = json.dumps(response_data, ensure_ascii=False)

            self.send_response(200)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            self.wfile.write(response_body.encode("utf-8"))

        except json.JSONDecodeError:
            response_data = {
                "status": "error",
                "message": "Body không phải JSON hợp lệ",
            }

            response_body = json.dumps(response_data, ensure_ascii=False)

            self.send_response(400)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            self.wfile.write(response_body.encode("utf-8"))


server = HTTPServer(("0.0.0.0", 8080), MyHandler)

print("Server running at http://0.0.0.0:8080")

server.serve_forever()
