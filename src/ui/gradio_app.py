# src/ui/gradio_ui.py

import gradio as gr
# Importa el PollService
from src.services.poll_service import PollService
from typing import Optional, Dict, Any

class GradioUI:
    """
    Manages the Gradio user interface for the application.
    Interacts with services to fetch and display data.
    """
    def __init__(self, poll_service: PollService):
        """
        Initializes the GradioUI with necessary services.

        Args:
            poll_service: The PollService instance.
        """
        print("GradioUI initialized.") # Mensaje de depuración
        self._poll_service = poll_service # Guarda la instancia del servicio

        # Define the Gradio Blocks interface
        self.interface = self._create_interface()

    def _create_interface(self):
        """
        Defines the layout and components of the Gradio interface.
        """
        print("Creating Gradio interface layout...")

        # --- Componentes para la Búsqueda de Usuario ---
        user_id_input = gr.Textbox(label="Introduce el User ID (UID) del usuario")
        get_tokens_button = gr.Button("Mostrar Tokens del Usuario")
        get_data_button = gr.Button("Mostrar Todos los Datos (JSON)")
        # Usaremos Textbox para la salida de tokens simples
        tokens_output = gr.Textbox(label="Resultado de Tokens", interactive=False)
        # Usaremos un componente tipo JSON o Textbox para los datos completos.
        # Un Textbox multilínea con formato JSON es a menudo más flexible en Gradio.
        data_output = gr.Textbox(label="Datos Completos del Usuario (JSON)", interactive=False, lines=10)


        # --- Componentes para la Interfaz de Encuestas (Mantén tu UI actual aquí) ---
        # Supongamos que tienes algo similar a esto para tus encuestas:
        # poll_question_input = gr.Textbox(label="Nueva pregunta de encuesta")
        # create_poll_button = gr.Button("Crear Encuesta")
        # ... otros componentes de encuestas ...

        # --- Definir la Estructura de la Interfaz usando gr.Blocks ---
        # gr.Blocks te da más control sobre el layout.
        with gr.Blocks() as interface_blocks:
            gr.Markdown("# Interfaz de tu Aplicación con Firebase") # Título principal

            # Sección de Búsqueda de Usuario
            with gr.Accordion("🔍 Buscar Información de Usuario", open=True): # Un acordeón para organizar
                gr.Markdown("Introduce el UID de Firebase Authentication para ver datos del usuario.")
                user_id_input.render() # Renderiza el Textbox de entrada de UID
                with gr.Row(): # Coloca los botones uno al lado del otro
                    get_tokens_button.render()
                    get_data_button.render()
                tokens_output.render() # Renderiza el Textbox de salida de tokens
                data_output.render() # Renderiza el Textbox de salida de datos JSON

            # Sección de Encuestas (Añade aquí tus componentes actuales de encuestas)
            with gr.Accordion("📊 Gestión de Encuestas", open=False): # Otro acordeón para encuestas
                gr.Markdown("Aquí irán tus controles para gestionar encuestas.")
                # Ejemplo:
                # poll_question_input.render()
                # create_poll_button.render()
                # ... Renderiza aquí los otros componentes de encuestas ...


            # --- Conectar Eventos (Botones) a Funciones ---

            # Conectar el botón de "Mostrar Tokens"
            # Cuando se haga clic, llama a _handle_get_user_tokens
            # La entrada es user_id_input, la salida es tokens_output
            get_tokens_button.click(
                fn=self._handle_get_user_tokens, # La función que llamará
                inputs=[user_id_input],         # El componente que proporciona la entrada (el UID)
                outputs=[tokens_output]         # El componente donde se mostrará el resultado
            )

            # Conectar el botón de "Mostrar Todos los Datos"
            get_data_button.click(
                 fn=self._handle_get_user_data,  # Una función diferente para datos JSON
                 inputs=[user_id_input],
                 outputs=[data_output]           # La salida va al Textbox de datos completos
            )

            # --- Conectar Eventos de Encuestas (Conecta tus botones y entradas de encuestas aquí) ---
            # create_poll_button.click(
            #     fn=self._handle_create_poll, # Debes tener un método _handle_create_poll
            #     inputs=[poll_question_input],
            #     outputs=[...] # La salida correspondiente (mensaje de éxito, lista de encuestas, etc.)
            # )
            # ... Conecta otros eventos de encuestas ...


        print("Gradio interface layout created.")
        return interface_blocks # Devuelve los bloques definidos

    # --- Funciones que Gradio Llamará ---

    def _handle_get_user_tokens(self, user_id_input: str) -> str:

        print(f"GradioUI Handler: Called for user ID: {user_id_input}")
        if not user_id_input:
            return "Error: Por favor, introduce un User ID."

        # Llama al método del servicio. self._poll_service es la instancia que recibimos en __init__
        result_message = self._poll_service.get_user_tokens_string(user_id_input.strip()) # .strip() para quitar espacios
        print(f"GradioUI Handler: Service returned: {result_message}")
        return result_message

# src/ui/gradio_ui.py (Continuación de la clase GradioUI)

    # ... tus funciones _handle_get_user_tokens y otras ...

    def _handle_get_user_data(self, user_id_input: str) -> str:

         print(f"GradioUI Handler: Called for user data JSON for ID: {user_id_input}")
         if not user_id_input:
             return "Error: Por favor, introduce un User ID."

         # ¡Corrección clave aquí! Llama al método del servicio que ya devuelve el JSON formateado.
         # self._poll_service es la instancia que recibimos en __init__
         json_data_string = self._poll_service.get_user_data_json_display(user_id_input.strip()) # .strip() para quitar espacios

         print(f"GradioUI Handler: Service returned JSON string.")
         return json_data_string # Retorna directamente la cadena JSON del servicio

    

