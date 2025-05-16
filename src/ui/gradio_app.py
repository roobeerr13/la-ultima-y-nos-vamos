import gradio as gr  # Corrected import
from src.controllers.ui_controller import UIController

def create_ui(ui_controller: UIController):
    def vote_wrapper(poll_id: str, username: str, option: str) -> str:
        try:
            ui_controller.vote(poll_id, username, option)
            return "Vote registered successfully!"
        except ValueError as e:
            return f"Error: {e}"

    demo = gr.Interface(
        fn=vote_wrapper,
        inputs=[
            gr.Textbox(label="Poll ID"),
            gr.Textbox(label="Username"),
            gr.Textbox(label="Option")
        ],
        outputs="text",
        title="StreamApp Voting System",
        description="Enter the Poll ID, your username, and your voting option."
    )
    return demo