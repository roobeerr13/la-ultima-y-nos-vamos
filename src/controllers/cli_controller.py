import cmd
from src.services.poll_service import PollService  # Corrected import
from src.services.user_service import UserService
from src.services.nft_service import NFTService

class CLIController(cmd.Cmd):
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService):
        super().__init__()
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.prompt = "(StreamApp) "

    def do_create_poll(self, line: str) -> None:
        args = line.split("|")
        if len(args) != 3:
            print("Usage: create_poll <question>|<options>|<duration>")
            return
        question, options, duration = args[0], args[1].split(","), int(args[2])
        poll = self.poll_service.create_poll(question, options, duration)
        print(f"Poll created: {poll.id}")

    def do_vote(self, line: str) -> None:
        poll_id, username, option = line.split()
        try:
            self.poll_service.vote(poll_id, username, option)
            print("Vote registered")
        except ValueError as e:
            print(f"Error: {e}")

    def do_quit(self, line: str) -> bool:
        return True