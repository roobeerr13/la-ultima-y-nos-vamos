from dataclasses import dataclass
from datetime import datetime  # Added import

@dataclass
class Vote:
    poll_id: str
    username: str
    option: str
    timestamp: datetime