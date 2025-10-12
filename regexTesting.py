import re
from datetime import datetime
target_string = "http://localhost:8080/quotes?author=gandhi&search=change&limit=2"
matches = re.findall(r"(author|search|limit)=(\w+)",target_string)

web_url = "http://localhost:8080/quotes/2"
target_id = re.search(r"http://localhost:8080dsd/quotes/(\w+)", web_url)
demo = {"text": "This is a raw text"}
current_datetime = datetime.now()
print(type(current_datetime.strftime("%d-%m-%Y %H:%M:%S")))
