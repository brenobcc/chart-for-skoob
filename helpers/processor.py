from .core_functions import *
from flask import send_file

def startProcess(user_id, columns, lines, paste_star):

    current_year = datetime.now().year

    response = mockFirstPageResponse(user_id, current_year)

    try:
        #fazer tratamento disso depois
        current_year = 2024
    except NameError:
        print(f"Em {current_year} há registros")

    print(response.status_code)

    if response.status_code == 200:
        response_json = response.json()
        # with open("log.json", "w", encoding="utf-8") as file:
        #      json.dump(response_json, file, indent=4, ensure_ascii=False)

        book_quantity = columns * lines

        total_read_books = totalReadBooks(user_id)
        if total_read_books < book_quantity:
            exit(f"Você tem apenas {total_read_books} livros lidos.")

        try:
           # inicio = time.time()

            chart_imgs = createByteImageArray(user_id, response_json, book_quantity, current_year, paste_star)

            grid = createGrid(columns, lines, chart_imgs)

            grid_io = io.BytesIO()
            grid.save(grid_io, 'PNG')  # Salva a imagem no buffer em formato PNG
            grid_io.seek(0)  # Move o ponteiro para o início do buffer

            return grid_io

           # fim = time.time()
            
           # print(fim - inicio)
        except Exception as e:
            print(e)