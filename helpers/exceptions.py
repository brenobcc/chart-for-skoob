# Invalid User (Code #1)
class InvalidUserException(Exception):
    def __init__(self, user_id, message="Usuario não encontrado!"):
        self.user_id = user_id
        self.message = message
        super().__init__(f"{user_id}: {message}")