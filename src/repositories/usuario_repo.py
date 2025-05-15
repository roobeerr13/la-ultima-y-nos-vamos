# src/repositories/usuario_repo.py
import json
from typing import Optional, List
from src.models.usuario import User

class UsuarioRepository:
    def __init__(self, file_path: str = "data/users.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        try:
            with open(self.file_path, "r") as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, "w") as f:
                json.dump({"users": []}, f)

    def save_user(self, user: User):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            data["users"].append({
                "username": user.username,
                "password_hash": user.password_hash,
                "tokens": user.tokens
            })
            f.seek(0)
            json.dump(data, f, indent=2)

    def get_user(self, username: str) -> Optional[User]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
            for u in data["users"]:
                if u["username"] == username:
                    return User(
                        username=u["username"],
                        password_hash=u["password_hash"],
                        tokens=u["tokens"]
                    )
        return None

    def update_user(self, user: User):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            for i, u in enumerate(data["users"]):
                if u["username"] == user.username:
                    data["users"][i] = {
                        "username": user.username,
                        "password_hash": user.password_hash,
                        "tokens": user.tokens
                    }
                    break
            f.seek(0)
            json.dump(data, f, indent=2)

    def get_all_usernames(self) -> List[str]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
            return [u["username"] for u in data["users"]]