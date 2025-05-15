# src/models/encuesta.py
from datetime import datetime
from uuid import uuid4
from typing import List, Dict

class Poll:
    def __init__(self, question: str, options: List[str], duration_seconds: int, poll_type: str = "simple"):
        self.id = str(uuid4())
        self.question = question
        self.options = options
        self.votes: Dict[str, int] = {opt: 0 for opt in options}  # option -> vote count
        self.voters: set = set()  # Track users who voted
        self.state = "active"
        self.created_at = datetime.now()
        self.duration = duration_seconds
        self.type = poll_type

    def is_active(self) -> bool:
        if self.state != "active":
            return False
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed <= self.duration

    def close(self):
        self.state = "closed"