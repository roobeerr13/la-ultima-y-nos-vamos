import json
from typing import Optional

class UserRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, user: dict) -> None:
        data = self._load_data()
        data[user["username"]] = user
        self._save_data(data)

    def find_by_username(self, username: str) -> Optional[dict]:
        data = self._load_data()
        return data.get(username)

    def _load_data(self) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_data(self, data: dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)