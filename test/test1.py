import requests
url = "http://127.0.0.1:8000/txtstream/"
response = requests.get(
    url,
    stream=True
)

for chunk in response.iter_content(1024):
    if chunk:
        print(str(chunk, encoding="utf-8"), end=" ", flush=True)
        