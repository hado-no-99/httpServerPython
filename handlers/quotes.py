from http.server import BaseHTTPRequestHandler
import json
import re
from datetime import datetime
from database.storage import quotes
from utils.helpers import Helpers
from models.quote_methods import Quote

class SimpleRequestHandler(BaseHTTPRequestHandler, Quote, Helpers):
    def do_GET(self):
        if self.path == "/" or self.path == "/home":
            message = "Welcome to the Quotes Server"
            self.send_server_response(200, message, "text/plain")

        elif self.path == "/about":
            message = json.dumps({"message" : "This is about us"})
            self.send_server_response(200, message, "application/json")

        elif self.path.startswith("/quotes"):
            # Handling query strings
            self.get_quotes()

    
    def do_POST(self):
        if self.path == "/quotes":
            self.post_quotes()

    def do_PUT(self):
        if self.path.startswith("/quotes"):
            self.put_quotes()

            
    def do_DELETE(self):
        if self.path.startswith("/quotes"):
            self.delete_quotes()
    