import matplotlib.pyplot as plt
import gradio as gr
from src.services.poll_service import PollService

class DashboardService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service

    def generate_dashboard(self):
        polls = self.poll_service.poll_repo.get_all("polls")
        num_polls = len(polls)
        num_votes = sum(len(p["votes"]) for p in polls if "votes" in p)
        plt.bar(["Encuestas", "Votos"], [num_polls, num_votes])
        plt.title("Estadísticas del Sistema")
        plt.savefig("dashboard.png")
        plt.close()
        return gr.Image("dashboard.png")