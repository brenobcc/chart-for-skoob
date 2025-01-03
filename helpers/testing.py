from core_functions import *

print("Recebendo dados...")

user_id = #test
columns = 8
lines = 4

total_grid_books = columns * lines

paste_star = False

current_year = 2025

print("Separando por ano...")
total_read_books, read_years = totalReadBooksAndYears(user_id, total_grid_books, current_year)

if total_read_books < total_grid_books:
    exit(f"Quantidade insuficiente de livros. {total_read_books} de {total_grid_books} necessários.")
        # with open("log.json", "w", encoding="utf-8") as file:
        #      json.dump(response_json, file, indent=4, ensure_ascii=False)

book_quantity = columns * lines
print(f"Grid: {book_quantity} livros")

    
    # if total_read_books < book_quantity:
    #     print(f"Você tem apenas {total_read_books} livros lidos.")


try:
    inicio = time.time()
    
    print("Gerando chart...")
    chart_imgs = createByteImageArray(user_id, read_years, paste_star)

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