from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService

class UIController:
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service

    def create_poll(self, question: str, options: str, duration: str) -> str:
        try:
            options_list = [opt.strip() for opt in options.split(",")]
            duration_int = int(duration)
            poll = self.poll_service.create_poll(question, options_list, duration_int)
            return f"Poll created: {poll.id}"
        except ValueError as e:
            return f"Error: {e}"

    def vote(self, poll_id: str, username: str, option: str) -> str:
        try:
            self.poll_service.vote(poll_id, username, option)
            return "Vote registered successfully!"
        except ValueError as e:
            return f"Error: {e}"

    def login(self, username: str, password: str) -> str:
        try:
            return self.user_service.login(username, password)
        except ValueError as e:
            return f"Error: {e}"

    def register(self, username: str, password: str) -> str:
        try:
            self.user_service.register(username, password)
            return "User registered successfully!"
        except ValueError as e:
            return f"Error: {e}"