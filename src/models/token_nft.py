# src/models/token_nft.py
from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TokenNFT:
    token_id: str = str(uuid4())
    owner: str
    poll_id: str
    option: str
    issued_at: datetime