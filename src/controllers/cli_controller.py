import cmd
from src.services.poll_service import PollService
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
        # Join parts split by | to handle cases where question contains |
        parts = line.split("|")
        if len(parts) < 3 or not all(parts):
            print("Usage: create_poll <question>|<options>|<duration>")
            return
        # Extract duration (last part), options (second-to-last part), and question (everything else)
        try:
            duration = int(parts[-1].strip())
            options_str = parts[-2].strip()
            question = "|".join(parts[:-2]).strip()
            if not question or not options_str:
                print("Usage: create_poll <question>|<options>|<duration>")
                return
            options = [opt.strip() for opt in options_str.split(",") if opt.strip()]
            if not options:
                print("Usage: create_poll <question>|<options>|<duration>")
                return
            poll = self.poll_service.create_poll(question, options, duration)
            print(f"Poll created: {poll.id}")
        except ValueError:
            print("Usage: create_poll <question>|<options>|<duration> (duration must be an integer)")

    def do_vote(self, line: str) -> None:
        parts = line.split()
        if len(parts) != 3:
            print("Usage: vote <poll_id> <username> <option>")
            return
        try:
            poll_id, username, option = parts
            self.poll_service.vote(poll_id, username, option)
            print("Vote registered")
        except ValueError as e:
            print(f"Error: {e}")

    def do_quit(self, line: str) -> bool:
        return True