import requests
import time
url = "http://127.0.0.1:8000/chat/?prompt=What is insurance?"
response = requests.get(
    url,
    stream=True,
    headers={"accept": "application/json"},
)

for chunk in response.iter_content(chunk_size=10):
    if chunk:
        print(str(chunk, encoding="utf-8"), end="", flush=True)
        