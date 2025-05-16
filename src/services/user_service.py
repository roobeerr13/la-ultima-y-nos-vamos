from .usuario import User
from ..repositories.usuario_repo import UserRepository
import bcrypt

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, username: str, password: str) -> User:
        if self.user_repo.find_by_username(username):
            raise ValueError("Username exists")
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(username=username, password_hash=password_hash, token_ids=[])
        self.user_repo.save(user)
        return user

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.find_by_username(username)
        if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            raise ValueError("Invalid credentials")
        return str(uuid4())  # Session token