from abc import ABC, abstractmethod
from .encuesta import Poll

class PollFactory(ABC):
    @abstractmethod
    def create_poll(self, question: str, options: List[str], duration: int) -> Poll:
        pass

class SimplePollFactory(PollFactory):
    def create_poll(self, question: str, options: List[str], duration: int) -> Poll:
        return Poll(id=str(uuid4()), question=question, options=options, votes={}, status="active", created_at=datetime.now(), duration_seconds=duration)