# src/ui/gradio_ui.py

import gradio as gr
# Importa el PollService (o UserService si decides crearlo)
from src.services.poll_service import PollService # Asegúrate que esta ruta es correcta
from typing import Optional, Dict, Any # Importa tipos si los usas en los manejadores

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
        print("GradioUI: Initializing...")
        # Guarda la instancia del servicio que fue inyectada
        self._poll_service = poll_service

        # Define y crea la interfaz de Gradio Blocks al inicializar la clase
        self.interface = self._create_interface()
        print("GradioUI: Interface created.")


    def _create_interface(self):
        """
        Defines the layout and components of the Gradio interface using gr.Blocks.
        Returns the configured gr.Blocks object.
        """
        print("GradioUI: Defining interface layout...")

        # --- Define los Componentes de UI ---

        # Componentes para la Búsqueda de Usuario
        user_id_input = gr.Textbox(label="Introduce el User ID (UID) de Firebase", placeholder="Ej: p1O2w3e4r5t6y7U8i9o0...")
        get_tokens_button = gr.Button("Mostrar Tokens del Usuario")
        get_data_button = gr.Button("Mostrar Todos los Datos (JSON)")

        # Componentes de salida para la Búsqueda de Usuario
        # Usamos Textbox para la salida de tokens simples (cadena)
        tokens_output = gr.Textbox(label="Resultado de Tokens", interactive=False, lines=1)
        # Usamos Textbox para la salida de datos JSON completos.
        # Configurado para ser multilínea y no interactivo.
        data_output = gr.Textbox(label="Datos Completos del Usuario (JSON)", interactive=False, lines=10)


        # Componentes para la Interfaz de Encuestas (EJEMPLOS - ADAPTA ESTO A TU UI ACTUAL)
        # Si ya tienes componentes para encuestas, colócalos aquí.
        # Por ejemplo:
        # poll_question_input = gr.Textbox(label="Pregunta de la nueva encuesta")
        # create_poll_button = gr.Button("Crear Encuesta")
        # poll_list_output = gr.Textbox(label="Lista de Encuestas Existentes", interactive=False)


        # --- Define la Estructura de la Interfaz usando gr.Blocks ---
        # gr.Blocks te da control granular sobre el layout y la interconexión de eventos.
        with gr.Blocks() as interface_blocks:
            gr.Markdown("# 👋 ¡Bienvenido a tu App con Firebase! 👋") # Título principal

            # Sección de Búsqueda de Usuario organizada en un Acordeón
            with gr.Accordion("👤 Buscar Información de Usuario", open=True):
                gr.Markdown("Introduce el **UID** de un usuario de Firebase Authentication para ver su información guardada en Firestore.")
                user_id_input.render() # Renderiza el Textbox de entrada para el UID
                with gr.Row(): # Organiza los dos botones en una fila
                    get_tokens_button.render()
                    get_data_button.render()
                tokens_output.render() # Renderiza el Textbox de salida de Tokens
                data_output.render() # Renderiza el Textbox de salida de Datos JSON

            # Sección para la Gestión de Encuestas (ADAPTA ESTO A TU UI ACTUAL)
            # Organizada en otro Acordeón. Puedes empezar cerrado (open=False).
            with gr.Accordion("📊 Gestión de Encuestas", open=False):
                 gr.Markdown("Aquí irán los controles y la visualización para tus encuestas.")
                 # EJEMPLOS (ADAPTA/AÑADE TUS COMPONENTES REALES DE ENCUESTAS AQUÍ):
                 # poll_question_input.render()
                 # create_poll_button.render()
                 # gr.Markdown("## Encuestas Existentes")
                 # poll_list_output.render()


            # --- Conectar Eventos de Componentes a Funciones Manejadoras ---
            # Usamos el método .click() del componente (el botón)
            # fn: La función Python que se ejecuta
            # inputs: Lista de componentes cuyos valores se pasan como argumentos a 'fn'
            # outputs: Lista de componentes que se actualizan con los valores devueltos por 'fn'

            # Conectar el botón "Mostrar Tokens del Usuario"
            get_tokens_button.click(
                fn=self._handle_get_user_tokens, # Llama al método interno de esta clase
                inputs=[user_id_input],         # Toma el texto del input de UID
                outputs=[tokens_output]         # Actualiza el Textbox de tokens
            )

            # Conectar el botón "Mostrar Todos los Datos (JSON)"
            get_data_button.click(
                 fn=self._handle_get_user_data,  # Llama al método interno para datos JSON
                 inputs=[user_id_input],         # Toma el texto del input de UID
                 outputs=[data_output]           # Actualiza el Textbox de datos JSON
            )

            # Conectar Eventos de Encuestas (ADAPTA ESTO A TUS BOTONES DE ENCUESTAS)
            # Si tienes un botón para crear encuestas, conéctalo a tu método de servicio correspondiente:
            # create_poll_button.click(
            #     fn=self._handle_create_poll, # Debes implementar este método en GradioUI
            #     inputs=[poll_question_input], # Toma la pregunta del input
            #     outputs=[poll_list_output] # Ejemplo: actualiza la lista de encuestas
            # )
            # Asegúrate de que los métodos _handle_... para encuestas existan en esta clase
            # y que llamen a los métodos correspondientes en self._poll_service.


        print("GradioUI: Interface layout defined.")
        return interface_blocks # Devuelve el objeto Blocks configurado


    # --- Funciones Manejadoras Llamadas por Gradio ---
    # Estas funciones reciben los valores de los 'inputs' y devuelven los valores para los 'outputs'.
    # NOTA: Siempre reciben 'self' porque son métodos de instancia de la clase GradioUI.

    def _handle_get_user_tokens(self, user_id_input: str) -> str:
        """
        Handles the button click to fetch and display user tokens.
        Calls the PollService to get the formatted token string.

        Args:
            user_id_input: The text value from the user ID input Textbox.

        Returns:
            A string to display in the tokens_output Textbox.
        """
        print(f"GradioUI Handler (_handle_get_user_tokens): Received user ID: '{user_id_input}'.")
        if not user_id_input or not user_id_input.strip():
            return "Error: Por favor, introduce un User ID válido."

        # Llama al método del servicio. self._poll_service es la instancia inyectada.
        # strip() elimina espacios al inicio/final que el usuario pudiera haber introducido.
        result_message = self._poll_service.get_user_tokens_string(user_id_input.strip())
        print(f"GradioUI Handler (_handle_get_user_tokens): Service returned message.")
        return result_message # Retorna la cadena formateada por el servicio

    def _handle_get_user_data(self, user_id_input: str) -> str:
        """
        Handles the button click to fetch and display all user data as a JSON string.
        Calls the PollService to get the JSON formatted data string.

        Args:
            user_id_input: The text value from the user ID input Textbox.

        Returns:
            A JSON formatted string or an error/not found message string.
        """
        print(f"GradioUI Handler (_handle_get_user_data): Received user ID: '{user_id_input}'.")
        if not user_id_input or not user_id_input.strip():
            return "Error: Por favor, introduce un User ID válido."

        # Llama al método del servicio que ya devuelve la cadena JSON formateada.
        # self._poll_service es la instancia inyectada.
        json_data_string = self._poll_service.get_user_data_json_display(user_id_input.strip())
        print(f"GradioUI Handler (_handle_get_user_data): Service returned JSON string.")
        return json_data_string # Retorna directamente la cadena JSON del servicio


    # --- Método para Lanzar la Interfaz ---

    def launch(self, **kwargs):
        """
        Launches the Gradio interface instance (the gr.Blocks object).
        Any keyword arguments are passed directly to the underlying interface.launch().
        """
        print("GradioUI: Launching interface...")
        # Llama al método launch() del objeto gr.Blocks que creamos en _create_interface
        self.interface.launch(**kwargs)
        print("GradioUI: Interface launched.")


# NOTA: No ejecutes Gradio directamente aquí si app.py es el punto de entrada.
# app.py se encargará de instanciar GradioUI y llamar a launch().

