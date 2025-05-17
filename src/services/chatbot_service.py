from transformers import pipeline
from src.services.poll_service import PollService

class ChatbotService:
    def __init__(self, poll_service):
        self.poll_service = poll_service
        # Integraremos Hugging Face aquí cuando me indiques el modelo

    def respond_to_query(self, user_input):
        return "Chatbot no configurado aún, usa un modelo de Hugging Face."