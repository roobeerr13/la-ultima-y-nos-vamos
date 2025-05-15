# src/models/usuario.py
from dataclasses import dataclass
from typing import List
import bcrypt

@dataclass
class User:
    username: str
    password_hash: str
    tokens: List[str] = None

    def __post_init__(self):
        self.tokens = self.tokens or []

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())