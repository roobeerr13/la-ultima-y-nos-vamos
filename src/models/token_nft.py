from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime

@dataclass
class TokenNFT:
    owner: str
    poll_id: str
    option: str
    token_id: str = str(uuid4())
    issued_at: datetime = datetime.now()

    @staticmethod
    def generate_id() -> str:
        return str(uuid4())