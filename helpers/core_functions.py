import requests
import requests_cache
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import io
from io import BytesIO
import time


requests_cache.install_cache("skoob_cache", expire_after=3600)
    
global headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def totalReadBooksAndYears(user_id, total_grid_books, current_year):
    target_year = current_year
    total_read_books = 0
    read_years = {}
    
    while (target_year > 2008 and total_grid_books > total_read_books):
        url = f"https://www.skoob.com.br/v1/bookcase/books/{user_id}/year:{target_year}/page:1/limit:1/"
        response = requests.get(url, headers=headers)
        response_json = response.json()

        if response_json["response"]:
            total_read_books_by_year = response_json["paging"]["total"]
            total_read_books += total_read_books_by_year
            
            read_years[f"{target_year}"] = total_read_books_by_year
        
        target_year -= 1

    return total_read_books, read_years

def mockPageResponseByYear(user_id, target_year, read_years):
    try:
        total_books_by_year = read_years[target_year]
        
        new_url = f"https://www.skoob.com.br/v1/bookcase/books/{user_id}/year:{target_year}/page:1/limit:{total_books_by_year}/"
        
        new_response = requests.get(new_url, headers=headers)
        
        return new_response

    except Exception as e:
        print(e)

def improveImageQuality(book_img):

    # Aumentar a nitidez
    enhancer = ImageEnhance.Sharpness(book_img)
    book_img = enhancer.enhance(1.5)

    # Aumentar o contraste
    enhancer = ImageEnhance.Contrast(book_img)
    book_img = enhancer.enhance(1)

    # Aumentar a saturação
    enhancer = ImageEnhance.Color(book_img)
    book_img = enhancer.enhance(1)

    # Aplicar um filtro de nitidez adicional (opcional)
    book_img = book_img.filter(ImageFilter.SHARPEN)

    return book_img

def openStar(star_type):
    # Estrela cheia
    if star_type == 0:
        img_star = Image.open("static/images/star-3.png").convert("RGBA")
        return img_star.resize((44, 44))
    
    # Meia estrela
    img_star = Image.open("static/images/half-star-3.png").convert("RGBA")
    return img_star.resize((44, 44))

def pasteStar(book_json, book_img):
    book_rating = book_json["ranking"]

    if book_rating == 0:
        return book_img

    if book_rating == 0.5:
        img_half_star = openStar(1)
        book_img.paste(img_half_star, (8, 575), img_half_star)

        return book_img

    for i in range(int(book_rating)):
        img_star = openStar(0)
        book_img.paste(img_star, (8 + (i * 50), 575), img_star)
    
    if type(book_rating) == float:
        img_half_star = openStar(1)
        book_img.paste(img_half_star, (8 + ((i + 1) * 50), 575), img_half_star)
    
    return book_img

def applyGradient(book_img):
    width = book_img.width
    height = book_img.height

    book_img = book_img.convert("RGBA")

    gradient = Image.new("L", (width, height), color=0)  #'L' (greyscale)
    draw = ImageDraw.Draw(gradient)

    gradient_height = int(height * 0.30)

    # Apply gradient lines
    for y in range(gradient_height):
        opacity = int(240 * (y / gradient_height))
        draw.line([(0, height - gradient_height + y), (width, height - gradient_height + y)], fill=opacity)

        gradient_alpha = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
        gradient_alpha.putalpha(gradient)

    return Image.alpha_composite(book_img, gradient_alpha)

def processImage(book_json, book_edition, paste_star):
        book_img = book_edition["capa_grande"]

        response_img = requests.get(book_img, headers=headers)

        # BytesIO converte para que Image consiga ler a requisição
        book_img_byte = Image.open(BytesIO(response_img.content))

        # Melhorar qualidade
        # book_img_byte = improve_image_quality(book_img_byte)

        new_size = (419, 633)

        book_img_resized = book_img_byte.resize(new_size, Image.Resampling.LANCZOS)

        if paste_star == True:
            book_img_resized = applyGradient(book_img_resized)
            book_img_resized = pasteStar(book_json, book_img_resized)

        book_img_resized = book_img_resized.convert("RGB")

        return book_img_resized

def createByteImageArray(user_id, book_quantity, read_years, paste_star):
    chart_imgs = {}
    
    book_count = 0
    
    for year in read_years:
        response = mockPageResponseByYear(user_id, year, read_years)
        response_json = response.json()
        total_read_books_by_year = response_json["paging"]["total"]
        
        # Algoritmo para varrer JSON
        for i in range(total_read_books_by_year - 1, - 1, -1):
            book_count += 1
            
            target_element = response_json["response"][i]

            book_edition = target_element["edicao"]
            book_name = book_edition["titulo"]
        
            book_img = processImage(target_element, book_edition, paste_star)

                # Salva dinamicamente a imagem em bytes em um array
            img_byte_value = io.BytesIO()

            book_img.save(img_byte_value, format="JPEG")
            chart_imgs[f"{book_count}-{book_name}"] = img_byte_value.getvalue()
            
            if book_count >= book_quantity:
                return chart_imgs

# Gerar grid de imagens
def createGrid(columns, lines, chart_imgs):
    new_size = (419, 633)

    chart_width = new_size[0] * columns
    chart_height = new_size[1] * lines

    book_quantity = columns * lines

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

    return grid