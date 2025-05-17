import cmd

class CLIController(cmd.Cmd):
    def __init__(self, poll_service, user_service, nft_service, chatbot_service):
        super().__init__()
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.prompt = "(StreamApp) "

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True