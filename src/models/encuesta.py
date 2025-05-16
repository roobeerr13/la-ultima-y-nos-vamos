from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class Poll:
    id: str
    question: str
    options: List[str]
    votes: Dict[str, List[str]]
    status: str
    created_at: datetime
    duration_seconds: int

    def is_active(self) -> bool:
        return self.status == "active" and (datetime.now() - self.created_at).total_seconds() < self.duration_seconds