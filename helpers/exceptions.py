# Invalid Input (Code #1)
class InvalidUserInput(Exception):
    def __init__(self, user_input):
        self.user_input = user_input
        super().__init__(f"Entrada de usuário inválida")
        
# Invalid User (Code #2)
class InvalidUserId(Exception):
    def __init__(self, user_id, message="Usuario não encontrado!"):
        self.user_id = user_id
        self.message = message
        super().__init__(f"{user_id}: {message}")

# Invalid User (Code #3)
class NotEnoughRegisteredBooks(Exception):
    def __init__(self, total_read_books, total_grid_books):
        self.total_read_books = total_read_books
        self.total_grid_books = total_grid_books
        super().__init__(f"Quantidade insuficiente de livros registrados ({total_read_books} de {total_grid_books})")
        