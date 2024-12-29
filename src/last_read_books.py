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
    response_json = response.json()
    # with open("logs/log.json", "w", encoding="utf-8") as file:
    #     json.dump(response_json, file, indent=4, ensure_ascii=False)

    n = 5

    try:
        for i in range(n):
            target_element = response_json["response"][i]
            book_edition = target_element["edicao"]
            book_name = book_edition["titulo"]
            book_image = book_edition["capa_pequena"]

            response_image = requests.get(book_image, headers=headers)

            with open(f"static/images/{book_name}.jpg", "wb") as file:
                file.write(response_image.content)
    except Exception as e:
        print(e)