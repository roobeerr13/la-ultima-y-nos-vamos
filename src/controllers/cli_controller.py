import cmd
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService

class CLIController(cmd.Cmd):
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService, chatbot_service: ChatbotService):
        super().__init__()
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.prompt = "(StreamApp) "

    def do_create_poll(self, line: str) -> None:
        parts = line.split("|")
        if len(parts) < 3 or not all(parts):
            print("Uso: create_poll <pregunta>|<opciones>|<duración>")
            return
        try:
            duration = int(parts[-1].strip())
            options_str = parts[-2].strip()
            question = "|".join(parts[:-2]).strip()
            if not question or not options_str:
                print("Uso: create_poll <pregunta>|<opciones>|<duración>")
                return
            options = [opt.strip() for opt in options_str.split(",") if opt.strip()]
            if not options:
                print("Uso: create_poll <pregunta>|<opciones>|<duración>")
                return
            poll = self.poll_service.create_poll(question, options, duration)
            print(f"Encuesta creada: {poll.id}")
        except ValueError:
            print("Uso: create_poll <pregunta>|<opciones>|<duración> (duración debe ser un entero)")

    def do_vote(self, line: str) -> None:
        parts = line.split()
        if len(parts) != 3:
            print("Error: Uso: vote <poll_id> <username> <opción>")
            return
        try:
            poll_id, username, option = parts
            token = self.poll_service.vote(poll_id, username, option)
            print(f"Voto registrado. Token generado: {token['token_id']}")
        except ValueError as e:
            print(f"Error: {e}")

    def do_trade_token(self, line: str) -> None:
        parts = line.split()
        if len(parts) != 3:
            print("Error: Uso: trade_token <token_id> <current_owner> <new_owner>")
            return
        try:
            token_id, current_owner, new_owner = parts
            self.nft_service.transfer_token(token_id, current_owner, new_owner)
            print("Token transferido con éxito")
        except ValueError as e:
            print(f"Error: {e}")

    def do_chat(self, line: str) -> None:
        try:
            response = self.chatbot_service.respond_to_query(line)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Error: {e}")

    def do_quit(self, line: str) -> bool:
        return True