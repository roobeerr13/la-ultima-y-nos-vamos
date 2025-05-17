import gradio as gr
from src.controllers.ui_controller import UIController

class GradioUI:
    def __init__(self, ui_controller: UIController):
        self.ui_controller = ui_controller

    def register_user(self, username: str, password: str):
        return f"Usuario {username} registrado correctamente"

    def login_user(self, username: str, password: str):
        return f"Usuario {username} inició sesión"

    def create_poll(self, question: str, options: str, duration: int):
        options_list = options.split(",")  
        return self.ui_controller.create_poll(question, options_list, duration)

    def vote_poll(self, poll_id: str, username: str, option: str):
        return self.ui_controller.vote(poll_id, username, option)

    def dashboard(self):
        return "Dashboard en construcción..."

    def chatbot_response(self, user_input: str):
        return f"Chatbot dice: {user_input}"

    def trade_token(self, token_id: str, new_owner: str):
        return f"Token {token_id} transferido a {new_owner}"

    def build_ui(self):
        with gr.Blocks() as demo:
            gr.Markdown("# StreamApp - Encuestas y NFTs")

            with gr.Tab("Registro / Inicio de Sesión"):
                username = gr.Textbox(label="Usuario")
                password = gr.Textbox(label="Contraseña", type="password")
                register_btn = gr.Button("Registrarse")
                login_btn = gr.Button("Iniciar Sesión")
                register_btn.click(self.register_user, inputs=[username, password], outputs="text")
                login_btn.click(self.login_user, inputs=[username, password], outputs="text")

            with gr.Tab("Crear Encuesta"):
                question = gr.Textbox(label="Pregunta")
                options = gr.Textbox(label="Opciones (separadas por comas)")
                duration = gr.Number(label="Duración (segundos)")
                create_poll_btn = gr.Button("Crear Encuesta")
                create_poll_btn.click(self.create_poll, inputs=[question, options, duration], outputs="text")

            with gr.Tab("Votar"):
                poll_id = gr.Textbox(label="ID de Encuesta")
                username_vote = gr.Textbox(label="Usuario")
                option_vote = gr.Textbox(label="Opción")
                vote_btn = gr.Button("Votar")
                vote_btn.click(self.vote_poll, inputs=[poll_id, username_vote, option_vote], outputs="text")

            with gr.Tab("Dashboard"):
                dashboard_btn = gr.Button("Ver Dashboard")
                dashboard_btn.click(self.dashboard, outputs="text")

            with gr.Tab("Chatbot"):
                user_input = gr.Textbox(label="Habla con el chatbot")
                chatbot_btn = gr.Button("Enviar")
                chatbot_btn.click(self.chatbot_response, inputs=[user_input], outputs="text")

            with gr.Tab("Trade de Tokens NFT"):
                token_id = gr.Textbox(label="ID del Token")
                new_owner = gr.Textbox(label="Nuevo Propietario")
                trade_btn = gr.Button("Transferir")
                trade_btn.click(self.trade_token, inputs=[token_id, new_owner], outputs="text")

        return demo

def create_ui(ui_controller):
    ui = GradioUI(ui_controller)
    return ui.build_ui()