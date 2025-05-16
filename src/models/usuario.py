from dataclasses import dataclass
from typing import List
import bcrypt

@dataclass
class User:
    username: str
    password_hash: str
    token_ids: List[str]

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()