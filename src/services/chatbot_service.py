from transformers import pipeline

class ChatbotService:
    def __init__(self, poll_service):
        self.poll_service = poll_service
        # Carga el modelo distilgpt2 con transformers
        self.pipe = pipeline("text-generation", model="distilgpt2")

    def get_active_polls(self):
        # Método auxiliar para obtener encuestas activas
        polls = self.poll_service.get_all("polls")
        return [poll for poll in polls if poll.get("status") == "active"]

    def respond_to_query(self, user_input):
        try:
            # Contexto con encuestas activas
            active_polls = self.get_active_polls()
            context = "Encuestas activas: " + ", ".join([p["question"] for p in active_polls]) if active_polls else "No hay encuestas activas."
            prompt = f"{context}\nUsuario: {user_input}\nBot:"
            response = self.pipe(prompt, max_length=100, num_return_sequences=1, truncation=True)
            return response[0]["generated_text"]
        except Exception as e:
            return f"Error en el chatbot: {str(e)}"