from helpers.core_functions import *
from datetime import datetime
import time
from helpers.exceptions import *

def startProcess(user_input, columns, lines, paste_star):
    print("Recebendo dados...")

    try:
        input_type = validateInput(user_input)
        user_id = getUserId(user_input, input_type)
        
        isUserValid(user_id)
        
        total_grid_books = columns * lines
        
        current_year = datetime.now().year

        print("Separando por ano...")
        total_read_books, read_years = totalReadBooksAndYears(user_id, total_grid_books, current_year)

        if total_read_books < total_grid_books:
            print(f"Quantidade insuficiente de livros. {total_read_books} de {total_grid_books} necessários.")
            return

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

            grid_io = io.BytesIO()
            grid.save(grid_io, 'PNG')  # Salva a imagem no buffer em formato PNG
            grid_io.seek(0)  # Move o ponteiro para o início do buffer
            
            return grid_io

            # return send_file(grid_io, mimetype='image/png', as_attachment=False,download_name='generated_image.png')

        except Exception as e:
            print(e)
            raise(e)
            
    except InvalidUserId as e:
        print(e)
        raise e
    except NotEnoughRegisteredBooks as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise(e)