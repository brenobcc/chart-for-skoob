from core_functions import *
from exceptions import *

print("Recebendo dados...")

user_id = #
try:
    isUserValid(user_id)
    
    columns = 10
    lines = 10

    total_grid_books = columns * lines

    paste_star = True

    current_year = 2025

    print("Separando por ano...")
    total_read_books, read_years = totalReadBooksAndYears(user_id, total_grid_books, current_year)

    if total_read_books < total_grid_books:
        exit(f"Quantidade insuficiente de livros. {total_read_books} de {total_grid_books} necessários.")

    book_quantity = columns * lines
    print(f"Grid: {book_quantity} livros")

    try:
        inicio = time.time()
        
        print("Gerando chart...")
        chart_imgs = createByteImageArray(user_id, book_quantity, read_years, paste_star)

        print("Colando grid...")
        grid = createGrid(columns, lines, chart_imgs)
        
        fim = time.time()     
        print(fim - inicio)
        
        print("Grid encerrado.")
        grid.show()

        grid_io = io.BytesIO()
        grid.save(grid_io, 'PNG')  # Salva a imagem no buffer em formato PNG
        grid_io.seek(0)  # Move o ponteiro para o início do buffer

        # return send_file(grid_io, mimetype='image/png', as_attachment=False,download_name='generated_image.png')

    except Exception as e:
        print(e)
except InvalidUserException as e:
    print(e)
    
except NotEnoughRegisteredBooks as e:
    print(e)