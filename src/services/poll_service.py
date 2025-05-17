from typing import List, Optional
from datetime import datetime

class PollService:
    def __init__(self, repo, tie_breaker, nft_service, user_service):
        self.repo = repo
        self.tie_breaker = tie_breaker
        self.nft_service = nft_service
        self.user_service = user_service

    def get_all(self, collection: str) -> List[dict]:
        return self.repo.get_all(collection)

    def create_poll(self, question, options, duration):
        poll_id = "poll_" + str(datetime.now().timestamp())
        poll_data = {
            "_id": poll_id,
            "question": question,
            "options": options.split(","),
            "votes": {},
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "duration_seconds": int(duration)
        }
        self.repo.save("polls", poll_id, poll_data)
        return poll_data