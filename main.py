from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/home":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            message = """
    <html>

       <head>

           <title>Python HTTP Server</title>

       </head>

       <body>

           <h1>Simple HTTP Server</h1>

           <p>Congratulations! The HTTP Server is working!

    Welcome to GeeksForGeeks</p>

       </body>

    </html>

"""
            self.wfile.write(message.encode())

        elif self.path == "/about":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            message = {"message" : "This is about us"}
            self.wfile.write(json.dumps(message).encode())

        


server_address = ("127.0.0.1", 8080)
my_http = HTTPServer(server_address, SimpleRequestHandler)
print("Server Running...")
my_http.serve_forever()
