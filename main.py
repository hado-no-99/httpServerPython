from http.server import HTTPServer, BaseHTTPRequestHandler
import json

quotes = [
    {"id": 1, "text": "Be the change you wish to see in the world", "author": "Gandhi"},
    {"id": 2, "text": "The only way to do great work is to love what you do", "author": "Steve Jobs"}
]

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

        else:
            self.send_response(404)
            message = "Invalid request"
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", int(len(message)))
            self.end_headers()
            self.wfile.write(message.encode())

    
    def do_POST(self):
        if self.path == "/quotes":
            try:
                input_size = int(self.headers.get('Content-Length', 0))
                if input_size == 0:
                    raise Exception("Data Required in POST Request")

                raw_input = self.rfile.read(input_size)
                json_input = raw_input.decode()
                dict_input = json.loads(json_input)

                if not "text" in dict_input or not "author" in dict_input:
                    raise Exception("Invalid Data") 

                quotes.append(dict_input)

                message_output = json.dumps({"status" : "success", "message" : "created"})
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(message_output)))
                self.end_headers()
                self.wfile.write(message_output.encode())

            except Exception as e:
                self.send_response(400)
                message_output = json.dumps({"status" : "error", "message" : str(e)})
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(message_output)))
                self.end_headers()
                self.wfile.write(message_output.encode())
            
        


server_address = ("127.0.0.1", 8080)
my_http = HTTPServer(server_address, SimpleRequestHandler)
print("Server Running...")
my_http.serve_forever()
