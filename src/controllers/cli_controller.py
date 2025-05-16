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
        args = line.split("|")
        if len(args) != 3 or not all(args):
            print("Usage: create_poll <question>|<options>|<duration>")
            return
        question, options_str, duration = args
        options = [opt.strip() for opt in options_str.split(",") if opt.strip()]
        if not options:
            print("Usage: create_poll <question>|<options>|<duration>")
            return
        try:
            duration = int(duration)
            poll = self.poll_service.create_poll(question, options, duration)
            print(f"Poll created: {poll.id}")
        except ValueError:
            print("Usage: create_poll <question>|<options>|<duration> (duration must be an integer)")

    def do_vote(self, line: str) -> None:
        try:
            poll_id, username, option = line.split()
            self.poll_service.vote(poll_id, username, option)
            print("Vote registered")
        except ValueError as e:
            if len(line.split()) != 3:
                print("Usage: vote <poll_id> <username> <option>")
            else:
                print(f"Error: {e}")

    def do_quit(self, line: str) -> bool:
        return True