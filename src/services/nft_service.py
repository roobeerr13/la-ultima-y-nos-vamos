import hashlib
from datetime import datetime
from src.repositories.firebase_repo import FirebaseRepository

class NFTService:
    def __init__(self, nft_repo: FirebaseRepository):
        self.nft_repo = nft_repo

    def mint_token(self, owner: str, poll_id: str, option: str) -> dict:
        vote_data = f"{poll_id}{owner}{option}{datetime.now()}"
        token_id = hashlib.sha256(vote_data.encode()).hexdigest()
        token = {
            "token_id": token_id,
            "owner": owner,
            "poll_id": poll_id,
            "option": option,
            "issued_at": datetime.now()
        }
        self.nft_repo.save("nfts", token_id, token)
        return token

    def transfer_token(self, token_id: str, current_owner: str, new_owner: str) -> None:
        token = self.nft_repo.find_by_id("nfts", token_id)
        if not token or token["owner"] != current_owner:
            raise ValueError("Token inválido o propietario incorrecto")
        token["owner"] = new_owner
        self.nft_repo.save("nfts", token_id, token)

    def find_by_id(self, token_id: str) -> dict:
        return self.nft_repo.find_by_id("nfts", token_id)