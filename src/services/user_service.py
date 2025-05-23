from src.models.usuario import User
from src.repositories.usuario_repo import UserRepository
from uuid import uuid4
import bcrypt

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, username: str, password: str) -> None:
        if self.user_repo.find_by_username(username):
            raise ValueError("Username already exists")
        password_hash = User.hash_password(password)
        user = User(username=username, password_hash=password_hash, token_ids=[])
        self.user_repo.save(user)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.find_by_username(username)
        if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            raise ValueError("Invalid credentials")
        return str(uuid4())  # Return a session token

    def add_token(self, username: str, token_id: str) -> None:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("User not found")
        user.token_ids.append(token_id)
        self.user_repo.save(user)

    def find_by_username(self, username: str) -> User:
        return self.user_repo.find_by_username(username)