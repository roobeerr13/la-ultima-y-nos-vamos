import gradio as gr
from ..controllers.ui_controller import UIController

def create_ui(ui_controller: UIController):
    def vote_wrapper(poll_id: str, username: str, option: str) -> str:
        return ui_controller.vote(poll_id, username, option)

    def create_poll_wrapper(question: str, options: str, duration: str) -> str:
        return ui_controller.create_poll(question, options, duration)

    def login_wrapper(username: str, password: str) -> str:
        return ui_controller.login(username, password)

    def register_wrapper(username: str, password: str) -> str:
        return ui_controller.register(username, password)

    demo = gr.TabbedInterface(
        [
            gr.Interface(
                fn=create_poll_wrapper,
                inputs=[
                    gr.Textbox(label="Question"),
                    gr.Textbox(label="Options (comma-separated)"),
                    gr.Textbox(label="Duration (seconds)")
                ],
                outputs="text",
                title="Create Poll"
            ),
            gr.Interface(
                fn=vote_wrapper,
                inputs=[
                    gr.Textbox(label="Poll ID"),
                    gr.Textbox(label="Username"),
                    gr.Textbox(label="Option")
                ],
                outputs="text",
                title="Vote in Poll"
            ),
            gr.Interface(
                fn=login_wrapper,
                inputs=[
                    gr.Textbox(label="Username"),
                    gr.Textbox(label="Password")
                ],
                outputs="text",
                title="Login"
            ),
            gr.Interface(
                fn=register_wrapper,
                inputs=[
                    gr.Textbox(label="Username"),
                    gr.Textbox(label="Password")
                ],
                outputs="text",
                title="Register"
            )
        ],
        ["Create Poll", "Vote", "Login", "Register"],
        title="StreamApp Voting System"
    )
    return demo