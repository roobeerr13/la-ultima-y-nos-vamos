from transformers import pipeline
from .poll_service import PollService

class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service
        self.chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

    def respond(self, username: str, message: str) -> str:
        if "who is winning" in message.lower():
            # Example of contextual response
            latest_poll = self.poll_service.get_latest_poll()
            if latest_poll:
                results = self.poll_service.get_partial_results(latest_poll.id)
                return f"Current leader: {max(results.items(), key=lambda x: x[1])[0]} with {results[max(results.items(), key=lambda x: x[1])[0]]} votes."
        response = self.chatbot(message)
        return response[-1]["generated_text"]