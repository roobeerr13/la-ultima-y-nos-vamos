class UIController:
    def __init__(self, poll_service, user_service, nft_service, chatbot_service, dashboard_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.dashboard_service = dashboard_service

    def create_poll(self, question, options, duration):
        return "Función create_poll no implementada aún"

    def vote(self, poll_id, username, option):
        return "Función vote no implementada aún"