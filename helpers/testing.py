from core_functions import *

user_id = 0
columns = 7
lines = 7

total_grid_books = columns * lines

paste_star = True

current_year = 2025

total_read_books, read_years = totalReadBooksAndYears(user_id, total_grid_books, current_year)

if total_read_books < total_grid_books:
    exit(f"Quantidade insuficiente de livros. {total_read_books} de {total_grid_books} necessários.")

response, current_year = 1, 2#mockFirstPageResponse(user_id, current_year)

print(response.status_code)

if response.status_code == 200:
    response_json = response.json()
        # with open("log.json", "w", encoding="utf-8") as file:
        #      json.dump(response_json, file, indent=4, ensure_ascii=False)

    book_quantity = columns * lines

    
    # if total_read_books < book_quantity:
    #     print(f"Você tem apenas {total_read_books} livros lidos.")


    try:
           # inicio = time.time()

        chart_imgs = createByteImageArray(user_id, response_json, book_quantity, current_year, paste_star)

        grid = createGrid(columns, lines, chart_imgs)
        
        grid.show()

        grid_io = io.BytesIO()
        grid.save(grid_io, 'PNG')  # Salva a imagem no buffer em formato PNG
        grid_io.seek(0)  # Move o ponteiro para o início do buffer

    # return send_file(grid_io, mimetype='image/png', as_attachment=False,download_name='generated_image.png')

           # fim = time.time()
            
           # print(fim - inicio)
    except Exception as e:
        print(e)