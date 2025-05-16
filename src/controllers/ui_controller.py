from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.services.dashboard_service import DashboardService

class UIController:
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService, chatbot_service: ChatbotService, dashboard_service: DashboardService):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.dashboard_service = dashboard_service

    def create_poll(self, question: str, options: str, duration: str) -> str:
        try:
            options_list = [opt.strip() for opt in options.split(",")]
            duration_int = int(duration)
            poll = self.poll_service.create_poll(question, options_list, duration_int)
            return f"Encuesta creada: {poll.id}"
        except ValueError as e:
            return f"Error: {e}"

    def vote(self, poll_id: str, username: str, option: str) -> str:
        try:
            token = self.poll_service.vote(poll_id, username, option)
            return f"Voto registrado con éxito! Token generado: {token['token_id']}"
        except ValueError as e:
            return f"Error: {e}"

    def login(self, username: str, password: str) -> str:
        try:
            token = self.user_service.login(username, password)
            return f"Inicio de sesión exitoso! Token: {token}"
        except ValueError as e:
            return f"Error: {e}"

    def register(self, username: str, password: str) -> str:
        try:
            token = self.user_service.register(username, password)
            return f"Usuario registrado con éxito! Token: {token}"
        except ValueError as e:
            return f"Error: {e}"