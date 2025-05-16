from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from src.models.encuesta import Poll
from src.repositories.firebase_repo import FirebaseRepository
from src.patterns.observer import Subject
from src.patterns.strategy import TieBreakerStrategy
from sentence_transformers import SentenceTransformer

class PollService(Subject):
    def __init__(self, poll_repo: FirebaseRepository, tie_breaker: TieBreakerStrategy, nft_service, user_service, chatbot_service):
        super().__init__()
        self.poll_repo = poll_repo
        self.tie_breaker = tie_breaker
        self.nft_service = nft_service
        self.user_service = user_service
        self.chatbot_service = chatbot_service
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_poll(self, question: str, options: List[str], duration: int) -> Poll:
        poll_id = str(uuid4())
        poll_data = {
            "id": poll_id,
            "question": question,
            "options": options,
            "votes": {},
            "status": "active",
            "created_at": datetime.now(),
            "duration_seconds": duration
        }
        self.poll_repo.save("polls", poll_id, poll_data)
        return Poll(**poll_data)

    def vote(self, poll_id: str, username: str, option: str) -> dict:
        poll_data = self.poll_repo.find_by_id("polls", poll_id)
        if not poll_data:
            raise ValueError("Encuesta no encontrada")
        poll = Poll(**poll_data)
        if not poll.is_active():
            raise ValueError("Encuesta no activa")
        if username in poll.votes:
            raise ValueError("El usuario ya votó")
        poll.votes[username] = [option]
        self.poll_repo.save("polls", poll.id, poll.__dict__)
        token = self.nft_service.mint_token(username, poll_id, option)
        self.user_service.add_token(username, token["token_id"])
        self.notify_observers(poll_id, "vote", {"username": username, "option": option})
        return token

    def close_poll(self, poll_id: str) -> None:
        poll_data = self.poll_repo.find_by_id("polls", poll_id)
        if not poll_data:
            raise ValueError("Encuesta no encontrada")
        poll = Poll(**poll_data)
        if poll.is_active():
            poll.status = "closed"
            self.poll_repo.save("polls", poll.id, poll.__dict__)
            self.notify_observers(poll_id, "close", self.get_final_results(poll_id))

    def get_final_results(self, poll_id: str) -> dict:
        poll_data = self.poll_repo.find_by_id("polls", poll_id)
        if not poll_data:
            raise ValueError("Encuesta no encontrada")
        poll = Poll(**poll_data)
        results = {opt: 0 for opt in poll.options}
        for votes in poll.votes.values():
            for opt in votes:
                results[opt] += 1
        max_votes = max(results.values())
        winners = [opt for opt, count in results.items() if count == max_votes]
        if len(winners) > 1:
            winner = self.tie_breaker.resolve(winners)
        else:
            winner = winners[0]
        return {"winner": winner, "results": results}

    def find_by_id(self, poll_id: str) -> Optional[Poll]:
        poll_data = self.poll_repo.find_by_id("polls", poll_id)
        return Poll(**poll_data) if poll_data else None

    def get_active_polls(self) -> List[Poll]:
        poll_data_list = self.poll_repo.get_all("polls")
        polls = [Poll(**data) for data in poll_data_list]
        return [poll for poll in polls if poll.is_active()]

    def get_embeddings(self, poll_id: str) -> list:
        poll = self.find_by_id(poll_id)
        if not poll:
            raise ValueError("Encuesta no encontrada")
        texts = [poll.question] + poll.options
        return self.model.encode(texts).tolist()