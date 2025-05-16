from transformers import pipeline
from src.services.poll_service import PollService

class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service
        self.chatbot = pipeline("text-generation", model="gpt2")

    def respond_to_query(self, user_input: str, poll_id: str = None) -> str:
        active_polls = self.poll_service.get_active_polls()
        context = "Active polls: " + ", ".join([p.question for p in active_polls]) if active_polls else "No active polls."
        if poll_id:
            poll = self.poll_service.find_by_id(poll_id)
            if poll:
                context += f" Poll {poll_id} question: {poll.question}, options: {', '.join(poll.options)}"
        prompt = f"{context}\nUser: {user_input}\nBot:"
        response = self.chatbot(prompt, max_length=50, num_return_sequences=1)
        return response[0]['generated_text']