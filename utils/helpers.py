import json
from datetime import datetime

class Helpers:
    def send_server_response(self, code, message="", type=""):
        self.send_response(code)
        if message:
            self.send_header("Content-Type", type)
            self.send_header("Content-Length", str(len(message)))
            self.end_headers()
            self.wfile.write(message.encode())
            return 
        self.end_headers()


    def get_base_list(self, filtered_quotes, quotes):
        if len(filtered_quotes):
            return filtered_quotes
        return quotes


    def validate_user_input(self, method="POST"):
        input_size = int(self.headers.get('Content-Length', 0))
        if input_size == 0:
            raise Exception(f"Data Required in {method} Request")

        raw_input = self.rfile.read(input_size)
        json_input = raw_input.decode()
        dict_input = json.loads(json_input)

        if method == "PUT":
            for key in dict_input:
                if key != "text" and key != "author":
                    raise Exception("Value can be either text or author")
                elif not dict_input[key] or len(dict_input[key]) > 500:
                    raise Exception("Input can't be empty or greater than 500")  
            return dict_input

        elif method == "POST":
            if not dict_input['text'] or not dict_input['author']:
                    raise Exception("Text/author values cant be empty")

            if len(dict_input['text']) > 500 or len(dict_input['author']) > 500:
                raise Exception("Text/author values cant exceed limit of 500 characters")

            return dict_input

        else:
            raise Exception("Invalid method specified")

    def add_timestamp(self):
        current_datetime = datetime.now()
        return current_datetime.strftime("%d-%m-%Y %H:%M:%S")