import requests
import json
from PIL import Image
import io
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

    columns, lines = map(int, input("Selecione o tamanho do grid:").split())
    books_quantity = columns * lines

    try:
        chart_imgs = {}

        # Algoritmo para varrer JSON
        for i in range(books_quantity):
            target_element = response_json["response"][i]
            book_edition = target_element["edicao"]
            book_name = book_edition["titulo"]
            book_img = book_edition["capa_pequena"]

            response_img = requests.get(book_img, headers=headers)

            # BytesIO converte para que Image consiga ler a requisição
            img_book = Image.open(BytesIO(response_img.content))

            new_size = (100, 150)
            book_img_resized = img_book.resize(new_size, Image.Resampling.LANCZOS)

            # Salva dinamicamente a imagem em bytes em um array
            img_byte_value = io.BytesIO()

            book_img_resized.save(img_byte_value, format="JPEG")
            chart_imgs[f"{book_name}"] = img_byte_value.getvalue()

        #Montar grid
        chart_width = 100 * columns
        chart_height = 150 * lines
        new_size = (100, 150)

        book_count = 0

        grid = Image.new("RGB", (chart_width, chart_height), (255, 255, 255))
        for book, image_bytes in chart_imgs.items():

            if book_count >= 3 * 4:
                break
            
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert("RGB")

            x = (book_count % columns) * new_size[0]
            y = (book_count // columns) * new_size[1]

            grid.paste(image, (x, y))

            book_count += 1

        grid.save("grid4x3.jpg")
    
    except Exception as e:
        print(e)
