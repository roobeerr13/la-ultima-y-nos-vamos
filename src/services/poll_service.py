from typing import List, Optional
from src.models.encuesta import Poll
from src.models.voto import Vote
from ..repositories.encuesta_repo import PollRepository
from ..patterns.observer import Subject
from ..patterns.strategy import TieBreakerStrategy

class PollService(Subject):
    def __init__(self, poll_repo: PollRepository, tie_breaker: TieBreakerStrategy):
        super().__init__()
        self.poll_repo = poll_repo
        self.tie_breaker = tie_breaker

    def create_poll(self, question: str, options: List[str], duration: int) -> Poll:
        poll = Poll(id=str(uuid4()), question=question, options=options, votes={}, status="active", created_at=datetime.now(), duration_seconds=duration)
        self.poll_repo.save(poll)
        return poll

    def vote(self, poll_id: str, username: str, option: str) -> None:
        poll = self.poll_repo.find_by_id(poll_id)
        if not poll or not poll.is_active():
            raise ValueError("Poll is not active")
        if username in poll.votes:
            raise ValueError("User already voted")
        poll.votes[username] = [option]
        self.poll_repo.save(poll)
        self.notify_observers(poll_id, "vote", {"username": username, "option": option})

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