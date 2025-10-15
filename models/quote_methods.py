from utils.helpers import Helpers
from database.storage import quotes
import re
import json


class Quote:
    def get_quotes(self):
        # Handling query strings
        query_start = re.search(r"?(author|search|limit)", self.path)
        matches = re.findall(r"(author|search|limit)=([^&]+)", self.path)
        print(matches)
        if query_start and len(matches):
            filtered_quotes = []
            for key, value in matches:
                base_list = self.get_base_list(filtered_quotes, quotes)

                if key == "author":
                    filtered_quotes = [quote for quote in base_list if quote['author'].lower() == value.lower().replace("+", "") and "Deleted" not in quote]
                    print(filtered_quotes)

                elif key == "search":
                    filtered_quotes = [quote for quote in base_list if value.lower().replace("+", "") in quote['text'].lower() and "Deleted" not in quote]
                    print(filtered_quotes)
                        
                elif key == "limit":
                    try:
                        filtered_quotes = base_list[:int(value)]
                        print(filtered_quotes)

                    except Exception:
                        continue
                
            self.send_server_response(200, json.dumps(filtered_quotes), "application/json")
            return
        
        elif self.path == "/quotes":
            filtered_quotes = [quote for quote in quotes if "Deleted" not in quotes]
            self.send_server_response(200, json.dumps(filtered_quotes), "application/json")

        else:
            message = "Invalid request"
            self.send_server_response(400, message, "text/plain")

