import requests
import json
from PIL import Image
from io import BytesIO
    
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

    n = 12

    try:
        paths = []

        # Algoritmo para varrer JSON
        for i in range(n):
            target_element = response_json["response"][i]
            book_edition = target_element["edicao"]
            book_name = book_edition["titulo"]
            book_image = book_edition["capa_pequena"]

            response_image = requests.get(book_image, headers=headers)

            # BytesIO converte para que Image consiga ler a requisição
            img_book = Image.open(BytesIO(response_image.content))

            new_size = (100, 150)
            img_book_resized = img_book.resize(new_size, Image.Resampling.LANCZOS)

            path = f"{book_name}_resized.jpg"
            img_book_resized.save(path)

            paths.append(path)

            # Salvar na pasta local
            # with open(f"static/images/{book_name}.jpg", "wb") as file:
            #     file.write(response_image.content)
    
    except Exception as e:
        print(e)

    #Montar grid
    largura = 100 * 4
    altura = 150 * 3
    new_size = (100, 150)

    grid = Image.new("RGB", (largura, altura), (255, 255, 255))
    for i, image in enumerate(paths):
        if i >= 3 * 4:
            break
        
        image = Image.open(image)

        x = (i % 4) * new_size[0]
        y = (i // 4) * new_size[1]

        grid.paste(image, (x, y))

    grid.save("grid4x3.jpg")