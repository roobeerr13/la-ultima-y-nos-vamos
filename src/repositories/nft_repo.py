import json
from typing import Optional
from src.models.token_nft import TokenNFT

class NFTRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, token: TokenNFT) -> None:
        data = self._load_data()
        data[token.token_id] = token.__dict__
        self._save_data(data)

    def find_by_id(self, token_id: str) -> Optional[TokenNFT]:
        data = self._load_data()
        token_data = data.get(token_id)
        if token_data:
            return TokenNFT(**token_data)
        return None

    def _load_data(self) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_data(self, data: dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)