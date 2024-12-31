import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
from io import BytesIO

# Colocar todos os livros lidos em uma única página
def mock_first_page(url, headers, user_id):
    response = requests.get(url, headers=headers)
    response_json = response.json()
    total_books = response_json["paging"]["total"]

    new_url = f"https://www.skoob.com.br/v1/bookcase/books/{user_id}/year:2024/page:1/limit:{total_books}/"

    return new_url

# Gerar grid de imagens
def create_grid(columns, lines, chart_imgs):
    new_size = (100, 150)

    chart_width = new_size[0] * columns
    chart_height = new_size[1] * lines

    book_count = 0

    grid = Image.new("RGB", (chart_width, chart_height), (255, 255, 255))

    for book, image_bytes in chart_imgs.items():

        if book_count >= book_quantity:
            break
            
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        x = (book_count % columns) * new_size[0]
        y = (book_count // columns) * new_size[1]

        grid.paste(image, (x, y))

        book_count += 1

    grid.save(f"grid{columns}x{lines}.jpg")

def paste_data(book_json, book_img):
    # Rating
    book_rating = book_json["ranking"]

    stars_paths = ["static/images/star.png", "static/images/half-star.png"]

    for i in range(int(book_rating)):
        img_star = Image.open("static/images/star-2.png").convert("RGBA")
        img_star = img_star.resize((12, 12))

        book_img.paste(img_star, (3 + (i * 12), 135), img_star)
    
    if type(book_rating) == float:
        img_half_star = Image.open("static/images/half-star-2.png").convert("RGBA")
        img_half_star = img_half_star.resize((12, 12))
        book_img.paste(img_half_star, (3 + ((i + 1) * 12), 135), img_half_star)
    
user_id = input("input your profile id: ")

url = f"https://www.skoob.com.br/v1/bookcase/books/{user_id}/year:2024/page:1/limit:1/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

new_url = mock_first_page(url, headers, user_id)

response = requests.get(new_url, headers=headers)

print(response.status_code)

if response.status_code == 200:
    response_json = response.json()
    # with open("logs/log.json", "w", encoding="utf-8") as file:
    #     json.dump(response_json, file, indent=4, ensure_ascii=False)

    columns, lines = map(int, input("Selecione o tamanho do grid:").split())
    book_quantity = columns * lines

    try:
        chart_imgs = {}
        total_books = response_json["paging"]["total"]
        # Algoritmo para varrer JSON
        for i in range(total_books - 1,  total_books - book_quantity - 1, -1):
            target_element = response_json["response"][i]

            book_edition = target_element["edicao"]
            book_name = book_edition["titulo"]
            book_img = book_edition["capa_pequena"]

            response_img = requests.get(book_img, headers=headers)

            # BytesIO converte para que Image consiga ler a requisição
            img_book = Image.open(BytesIO(response_img.content))

            new_size = (100, 150)
            book_img_resized = img_book.resize(new_size, Image.Resampling.LANCZOS)


            paste_data(target_element, book_img_resized)
            # Salva dinamicamente a imagem em bytes em um array
            img_byte_value = io.BytesIO()

            book_img_resized.save(img_byte_value, format="JPEG")
            chart_imgs[f"{book_name}"] = img_byte_value.getvalue()

        #Montar grid
        create_grid(columns, lines, chart_imgs)
        
    except Exception as e:
        print(e)