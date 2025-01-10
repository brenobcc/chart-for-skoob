# Invalid User (Code #1)
class InvalidUserException(Exception):
    def __init__(self, user_id, message="Usuario não encontrado!"):
        self.user_id = user_id
        self.message = message
        super().__init__(f"{user_id}: {message}")
        
class NotEnoughRegisteredBooks(Exception):
    def __init__(self, total_read_books, total_grid_books):
        self.total_read_books = total_read_books
        self.total_grid_books = total_grid_books
        super().__init__(f"Quantidade insuficiente de livros registrados ({total_read_books} de {total_grid_books})")