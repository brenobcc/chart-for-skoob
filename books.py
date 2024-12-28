import requests
import json

user_id = input("input your profile id: ")

url = f"https://www.skoob.com.br/v1/bookcase/books/{user_id}/year:2024/page:1/limit:36/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

print(response.status_code)

if response.status_code == 200:
    with open("log.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)