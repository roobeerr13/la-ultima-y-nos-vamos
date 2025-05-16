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

    def trade_token_wrapper(token_id: str, current_owner: str, new_owner: str) -> str:
        return ui_controller.nft_service.transfer_token(token_id, current_owner, new_owner)

    def chat_wrapper(user_input: str) -> str:
        return ui_controller.chatbot_service.respond_to_query(user_input)

    def dashboard_wrapper() -> gr.Image:
        return ui_controller.dashboard_service.generate_dashboard()

    demo = gr.TabbedInterface(
        [
            gr.Interface(
                fn=create_poll_wrapper,
                inputs=[
                    gr.Textbox(label="Pregunta"),
                    gr.Textbox(label="Opciones (separadas por comas)"),
                    gr.Textbox(label="Duración (segundos)")
                ],
                outputs="text",
                title="Crear Encuesta"
            ),
            gr.Interface(
                fn=vote_wrapper,
                inputs=[
                    gr.Textbox(label="ID de la Encuesta"),
                    gr.Textbox(label="Nombre de Usuario"),
                    gr.Textbox(label="Opción")
                ],
                outputs="text",
                title="Votar en Encuesta"
            ),
            gr.Interface(
                fn=login_wrapper,
                inputs=[
                    gr.Textbox(label="Nombre de Usuario"),
                    gr.Textbox(label="Contraseña")
                ],
                outputs="text",
                title="Iniciar Sesión"
            ),
            gr.Interface(
                fn=register_wrapper,
                inputs=[
                    gr.Textbox(label="Nombre de Usuario"),
                    gr.Textbox(label="Contraseña")
                ],
                outputs="text",
                title="Registrar Usuario"
            ),
            gr.Interface(
                fn=trade_token_wrapper,
                inputs=[
                    gr.Textbox(label="ID del Token"),
                    gr.Textbox(label="Propietario Actual"),
                    gr.Textbox(label="Nuevo Propietario")
                ],
                outputs="text",
                title="Tradear Token"
            ),
            gr.Interface(
                fn=chat_wrapper,
                inputs=gr.Textbox(label="Habla con el Bot"),
                outputs="text",
                title="Chatbot"
            ),
            gr.Interface(
                fn=dashboard_wrapper,
                inputs=None,
                outputs="image",
                title="Dashboard"
            )
        ],
        ["Crear Encuesta", "Votar", "Iniciar Sesión", "Registrar", "Tradear Token", "Chatbot", "Dashboard"],
        title="StreamApp Sistema de Votación"
    )
    return demo