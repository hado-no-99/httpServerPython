import re
from datetime import datetime
target_string = "http://localhost:8080/quotes?author=gandhi&search=change&limit=2"
matches = re.findall(r"(author|search|limit)=(\w+)",target_string)

text = "domain?search"
query_search = re.search(r"\?(author|search|limit)", text)
print(query_search)
