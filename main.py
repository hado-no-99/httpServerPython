from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
from datetime import datetime
from handlers.quotes import SimpleRequestHandler


server_address = ("127.0.0.1", 8080)
my_http = HTTPServer(server_address, SimpleRequestHandler)
print("Server Running...")
my_http.serve_forever()

