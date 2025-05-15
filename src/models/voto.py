# src/models/voto.py
from dataclasses import dataclass
from uuid import uuid4

@dataclass
class Vote:
    id: str = str(uuid4())
    poll_id: str
    username: str
    option: str
    timestamp: datetime