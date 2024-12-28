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
    with open("logs/log.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

    url_image = "https://img.skoob.com.br/xJfbW7PZFWAZ9BwV8v51a66C5DE=/100x0/center/top/filters:format(jpeg)/https://skoob.s3.amazonaws.com/livros/884818/PESSOAS_NORMAIS_1560341630884818SK1560341631B.jpg"

    response_image = requests.get(url_image, headers=headers)

    with open("images/normal-people.jpg", "wb") as file:
        file.write(response_image.content)