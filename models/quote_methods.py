from utils.helpers import Helpers
from database.storage import quotes
import re
import json


class Quote:
    def get_quotes(self):
        # Handling query strings
        query_start = re.search(r"\?(author|search|limit)", self.path)
        matches = re.findall(r"(author|search|limit)=([^&]+)", self.path)
        print(matches)
        if query_start and len(matches):
            filtered_quotes = []
            for key, value in matches:
                base_list = self.get_base_list(filtered_quotes, quotes)
                print(base_list)

                if key == "author":
                    filtered_quotes = [quote for quote in base_list if quote['author'].lower() == value.lower().replace("+", " ") and "Deleted" not in quote]
                    print(filtered_quotes)

                elif key == "search":
                    filtered_quotes = [quote for quote in base_list if value.lower().replace("+", " ") in quote['text'].lower() and "Deleted" not in quote]
                    print(filtered_quotes)
                        
                elif key == "limit":
                    try:
                        filtered_quotes = base_list[:int(value)]
                        print(filtered_quotes)

                    except Exception:
                        continue
            
            print(filtered_quotes)
            self.send_server_response(200, json.dumps(filtered_quotes), "application/json")
            return
        
        elif self.path == "/quotes":
            filtered_quotes = [quote for quote in quotes if "Deleted" not in quote]
            self.send_server_response(200, json.dumps(filtered_quotes), "application/json")

        else:
            message = "Invalid request"
            self.send_server_response(400, message, "text/plain")


    def post_quotes(self):
        try:
            dict_input = self.validate_user_input()

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


    def put_quotes(self):
        try:
            dict_input = self.validate_user_input(method="PUT")
            target_id = self.fetch_quote_id()

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
                    self.send_server_response(200, message_output, "application/json")
            
            raise Exception("Specified quote doesnt exists")

        except Exception as e:
            message_output = json.dumps({"status" : "error", "message" : str(e)})
            self.send_server_response(400, message_output, "application/json")


    def delete_quotes(self):
        try:
            target_id = self.fetch_quote_id()

            for quote in quotes:
                if quote['id'] == int(target_id):
                    quote["Deleted"] = "True"
                    quote["deleted_at"] = self.add_timestamp()
                    self.send_server_response(201)
                    return
            
            raise Exception("Specified quote doesnt exists")

        except Exception as e:
            message_output = json.dumps({"status" : "error", "message" : str(e)})
            self.send_server_response(400, message_output, "application/json")