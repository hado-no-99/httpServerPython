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
            try:
                input_size = int(self.headers.get('Content-Length', 0))
                if input_size == 0:
                    raise Exception("Data Required in POST Request")

                raw_input = self.rfile.read(input_size)
                json_input = raw_input.decode()
                dict_input = json.loads(json_input)
                
                if not dict_input['text'] or not dict_input['author']:
                    raise Exception("Text/author values cant be empty")

                if len(dict_input['text']) > 500 or len(dict_input['author']) > 500:
                    raise Exception("Text/author values cant exceed limit of 500 characters") 

                # adding id to quote
                id = quotes[-1].get('id', 0)
                dict_input['id'] = id + 1

                # adding created_at timestamp when a quote is created
                dict_input["created_at"] = self.add_timestamp()
                        
                quotes.append(dict_input)

                message_output = json.dumps({"status" : "success", "message" : "created"})
                self.send_server_response(201, message_output, "application/json")

            except Exception as e:
                message_output = json.dumps({"status" : "error", "message" : str(e)})
                self.send_server_response(400, message_output, "application/json")

    def do_PUT(self):
        if self.path.startswith("/quotes"):
            try:
                input_size = int(self.headers.get('Content-Length', 0))
                if input_size == 0:
                    raise Exception("Data Required in PUT Request")

                raw_input = self.rfile.read(input_size)
                json_input = raw_input.decode()
                dict_input = json.loads(json_input)

                for key in dict_input:
                    if key != "text" and key != "author":
                        raise Exception("Value can be either text or author")
                    elif not dict_input[key] or len(dict_input[key]) > 500:
                        raise Exception("Input can't be empty or greater than 500")


                target_id_search = re.search(r"/quotes/(\d+)", self.path)
                print(self.path, target_id_search)
                if not target_id_search:
                    raise Exception("Invalid quote id")

                target_id = target_id_search.group(1)

                for quote in quotes:
                    if quote['id'] == int(target_id):
                        print("inside condition")
                        print(dict_input)
                        if "text" in dict_input and "author" in dict_input:
                            print("matched author and text conditions")
                            quote['text'] = dict_input['text']
                            quote['author'] = dict_input['author']
                        elif "text" in dict_input:
                            print("Matched the text condition")
                            quote["text"] = dict_input["text"]
                        elif "author" in dict_input:
                            print("Matched the author condition")
                            quote["author"] = dict_input["author"]

                            
                        # adding/modifying the modified_at timestamp
                        quote['modified_at'] = self.add_timestamp()


                        message_output = json.dumps(quote)
                        self.send_server_response(200, message_output.encode(), "application/json")
                
                raise Exception("Specified quote doesnt exists")

            except Exception as e:
                message_output = json.dumps({"status" : "error", "message" : str(e)})
                self.send_server_response(400, message_output.encode(), "application/json")

            
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
    
    def add_timestamp(self):
        current_datetime = datetime.now()
        return current_datetime.strftime("%d-%m-%Y %H:%M:%S")