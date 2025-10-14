class Helpers:
    def send_server_response(self, code, message=None, type=None):
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
        
