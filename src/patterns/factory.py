from abc import ABC, abstractmethod
from uuid import uuid4
from datetime import datetime  # Ensure datetime is imported for use
from src.models.encuesta import Poll  # Corrected import

class PollFactory(ABC):
    @abstractmethod
    def create_poll(self, question: str, options: list[str], duration: int) -> Poll:
        pass

class SimplePollFactory(PollFactory):
    def create_poll(self, question: str, options: list[str], duration: int) -> Poll:
        return Poll(id=str(uuid4()), question=question, options=options, votes={}, status="active", created_at=datetime.now(), duration_seconds=duration)