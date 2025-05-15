# src/repositories/nft_repo.py
import json
from typing import Optional, List
from src.models.token_nft import TokenNFT
from datetime import datetime

class NFTRepository:
    def __init__(self, file_path: str = "data/nfts.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        try:
            with open(self.file_path, "r") as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, "w") as f:
                json.dump({"tokens": []}, f)

    def save_token(self, token: TokenNFT):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            data["tokens"].append({
                "token_id": token.token_id,
                "owner": token.owner,
                "poll_id": token.poll_id,
                "option": token.option,
                "issued_at": token.issued_at.isoformat()
            })
            f.seek(0)
            json.dump(data, f, indent=2)

    def get_token(self, token_id: str) -> Optional[TokenNFT]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
            for t in data["tokens"]:
                if t["token_id"] == token_id:
                    return TokenNFT(
                        token_id=t["token_id"],
                        owner=t["owner"],
                        poll_id=t["poll_id"],
                        option=t["option"],
                        issued_at=datetime.fromisoformat(t["issued_at"])
                    )
        return None

    def update_token(self, token: TokenNFT):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            for i, t in enumerate(data["tokens"]):
                if t["token_id"] == token.token_id:
                    data["tokens"][i] = {
                        "token_id": token.token_id,
                        "owner": token.owner,
                        "poll_id": token.poll_id,
                        "option": token.option,
                        "issued_at": token.issued_at.isoformat()
                    }
                    break
            f.seek(0)
            json.dump(data, f, indent=2)

    def get_user_tokens(self, username: str) -> List[TokenNFT]:
        tokens = []
        with open(self.file_path, "r") as f:
            data = json.load(f)
            for t in data["tokens"]:
                if t["owner"] == username:
                    tokens.append(TokenNFT(
                        token_id=t["token_id"],
                        owner=t["owner"],
                        poll_id=t["poll_id"],
                        option=t["option"],
                        issued_at=datetime.fromisoformat(t["issued_at"])
                    ))
        return tokens