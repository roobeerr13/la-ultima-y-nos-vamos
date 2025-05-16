from src.models.token_nft import TokenNFT
from src.repositories.nft_repo import NFTRepository
from datetime import datetime

class NFTService:
    def __init__(self, nft_repo: NFTRepository):
        self.nft_repo = nft_repo

    def mint_token(self, owner: str, poll_id: str, option: str) -> TokenNFT:
        token = TokenNFT(token_id=TokenNFT.generate_id(), owner=owner, poll_id=poll_id, option=option, issued_at=datetime.now())
        self.nft_repo.save(token)
        return token

    def transfer_token(self, token_id: str, current_owner: str, new_owner: str) -> None:
        token = self.nft_repo.find_by_id(token_id)
        if not token or token.owner != current_owner:
            raise ValueError("Invalid token or owner")
        token.owner = new_owner
        self.nft_repo.save(token)