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
            try:
                target_id_search = re.search(r"/quotes/(\d+)", self.path)
                if not target_id_search:
                    raise Exception("Invalid quote id")

                target_id = target_id_search.group(1)

                for quote in quotes:
                    if quote['id'] == int(target_id):
                        quote["Deleted"] = "True"
                        quote["deleted_at"] = self.add_timestamp()
                        self.send_server_response(201)
                        return
                
                raise Exception("Specified quote doesnt exists")

            except Exception as e:
                message_output = json.dumps({"status" : "error", "message" : str(e)})
                self.send_server_response(400, message_output.encode(), "application/json")
    
    