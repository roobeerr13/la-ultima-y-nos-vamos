import hashlib
import uuid
from src.repositories.usuario_repo import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, username: str, password: str) -> str:
        if self.user_repo.find_by_username(username):
            raise ValueError("El usuario ya existe")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        token = str(uuid.uuid4())
        user = {
            "username": username,
            "password_hash": password_hash,
            "token": token,
            "token_ids": []  # Para almacenar NFTs
        }
        self.user_repo.save(user)
        return token

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("Usuario no encontrado")
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if user["password_hash"] != hashed:
            raise ValueError("Credenciales inválidas")
        return user["token"]

    def add_token(self, username: str, token_id: str) -> None:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError("Usuario no encontrado")
        user["token_ids"].append(token_id)
        self.user_repo.save(user)