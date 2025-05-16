from typing import List, Optional
from datetime import datetime, timedelta
from uuid import uuid4
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.repositories.encuesta_repo import PollRepository
from src.patterns.observer import Subject
from src.patterns.strategy import TieBreakerStrategy

class PollService(Subject):
    def __init__(self, poll_repo: PollRepository, tie_breaker: TieBreakerStrategy):
        super().__init__()
        self.poll_repo = poll_repo
        self.tie_breaker = tie_breaker

    def create_poll(self, question: str, options: List[str], duration: int) -> Poll:
        poll = Poll(id=str(uuid4()), question=question, options=options, votes={}, status="active", created_at=datetime.now(), duration_seconds=duration)
        self.poll_repo.save(poll)
        return poll

    def vote(self, poll_id: str, username: str, option: str) -> dict:
        poll = self.poll_repo.find_by_id(poll_id)
        if not poll or not poll.is_active():
            raise ValueError("Encuesta no activa")
        if username in poll.votes:
            raise ValueError("El usuario ya votó")
        poll.votes[username] = [option]
        self.poll_repo.save(poll)
        token = self.nft_service.mint_token(username, poll_id, option)
        self.user_service.add_token(username, token["token_id"])
        self.notify_observers(poll_id, "vote", {"username": username, "option": option})
        return token

    def close_poll(self, poll_id: str) -> None:
        poll = self.poll_repo.find_by_id(poll_id)
        if poll and poll.is_active():
            poll.status = "closed"
            self.poll_repo.save(poll)
            self.notify_observers(poll_id, "close", self.get_final_results(poll_id))

    def get_final_results(self, poll_id: str) -> dict:
        poll = self.poll_repo.find_by_id(poll_id)
        if not poll:
            raise ValueError("Poll not found")
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
        return self.poll_repo.find_by_id(poll_id)

    def get_active_polls(self) -> List[Poll]:
        data = self.poll_repo._load_data()
        polls = []
        for poll_data in data.values():
            if 'created_at' in poll_data and isinstance(poll_data['created_at'], str):
                poll_data['created_at'] = datetime.fromisoformat(poll_data['created_at'])
            polls.append(Poll(**poll_data))
        return [poll for poll in polls if poll.is_active()]