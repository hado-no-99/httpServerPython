from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
from datetime import datetime

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

        elif self.path.startswith("/quotes"):
            # Handling query strings
            matches = re.findall(r"(author|search|limit)=([^&]+)", self.path)
            print(matches)
            if len(matches):
                filtered_quotes = []
                for key, value in matches:
                    if key == "author":
                        if len(filtered_quotes):
                            filtered_quotes = [quote for quote in filtered_quotes if value.lower() == quote['author'].lower() and "Deleted" not in quote]
                        else:
                            filtered_quotes = [quote for quote in quotes if quote['author'].lower() == value.lower() and "Deleted" not in quote]
                        print(filtered_quotes)

                    elif key == "search":
                        if len(filtered_quotes):
                            filtered_quotes = [quote for quote in filtered_quotes if value.lower() in quote['text'].lower() and "Deleted" not in quote]
                            print(filtered_quotes)
                        else:
                            filtered_quotes = [quote for quote in quotes if value.lower() in quote['text'].lower() and "Deleted" not in quote]
                            print(filtered_quotes)
                            
                    elif key == "limit":
                        try:
                            if len(filtered_quotes):
                                filtered_quotes = filtered_quotes[:int(value)]
                                filtered_quotes
                                print(filtered_quotes)
                            else:
                                filtered_quotes = quotes[:int(value)]
                                print(filtered_quotes)

                        except Exception:
                            continue
                    
                filtered_quotes_json = json.dumps(filtered_quotes)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(filtered_quotes_json)))
                self.end_headers()
                self.wfile.write(filtered_quotes_json.encode())
                return
            else:
                quotes_json = json.dumps(quotes)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(quotes_json)))
                self.end_headers()
                self.wfile.write(quotes_json.encode())
                return

        else:
            self.send_response(404)
            message = "Invalid request"
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(message)))
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
                

                if not "text" in dict_input:
                    raise Exception("No text option specified!")

                if not "author" in dict_input:
                    raise Exception("No author option specified!")

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


                        message_output = json.dumps({"status" : "success", "message" : "created"})
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(message_output)))
                        self.end_headers()
                        self.wfile.write(message_output.encode())
                        return()
                
                raise Exception("Specified quote doesnt exists")

            except Exception as e:
                self.send_response(400)
                message_output = json.dumps({"status" : "error", "message" : str(e)})
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(message_output)))
                self.end_headers()
                self.wfile.write(message_output.encode())

            
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
                        self.send_response(204)
                        self.end_headers()
                        return()
                
                raise Exception("Specified quote doesnt exists")

            except Exception as e:
                self.send_response(400)
                message_output = json.dumps({"status" : "error", "message" : str(e)})
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(message_output)))
                self.end_headers()
                self.wfile.write(message_output.encode())

    def add_timestamp(self):
        current_datetime = datetime.now()
        return current_datetime.strftime("%d-%m-%Y %H:%M:%S")
        


server_address = ("127.0.0.1", 8080)
my_http = HTTPServer(server_address, SimpleRequestHandler)
print("Server Running...")
my_http.serve_forever()

