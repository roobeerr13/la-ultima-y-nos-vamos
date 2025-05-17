import gradio as gr
from ..controllers.ui_controller import UIController


def create_ui(ui_controller):
    with gr.Blocks() as demo:
        gr.Markdown("# StreamApp con MongoDB")
        with gr.Row():
            question = gr.Textbox(label="Pregunta")
            options = gr.Textbox(label="Opciones (separadas por coma)")
            duration = gr.Number(label="Duración (segundos)")
        create_btn = gr.Button("Crear Encuesta")
        output = gr.Textbox(label="Resultado")
        create_btn.click(
            fn=ui_controller.create_poll,
            inputs=[question, options, duration],
            outputs=output
        )
    return demo

if __name__ == "__main__":
    ui_controller = UIController(None, None, None, None, None)  # Placeholder
    create_ui(ui_controller).launch()