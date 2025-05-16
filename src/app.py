# src/app.py

import google.auth
from google.cloud import firestore
from src.repositories.firebase_repo import FirebaseRepository
from src.services.poll_service import PollService
from src.ui.gradio_ui import GradioUI 
import argparse 

# --- Configuración ---
SERVICE_ACCOUNT_FILE = "src/serviceAccountKey.json"
PROJECT_ID = 'streamapp-19258'
DATABASE_ID = 'streamapp'

# --- Inicialización de la Aplicación ---
def main():
    print("Initializing application...")

    # Opcional: Argument parsing si usas --ui como en tu comando de error
    parser = argparse.ArgumentParser(description="Launch application UI or CLI.")
    parser.add_argument('--ui', action='store_true', help='Launch Gradio UI')
    args = parser.parse_args()

    # 1. Cargar credenciales y crear cliente de Firestore (UNA VEZ)
    try:
        print(f"Loading credentials from {SERVICE_ACCOUNT_FILE}...")
        credentials, project = google.auth.load_credentials_from_file(SERVICE_ACCOUNT_FILE)
        print("Credentials loaded.")

        print(f"Initializing Firestore client for project '{PROJECT_ID}', database '{DATABASE_ID}'...")
        db_client = firestore.Client(
            project=PROJECT_ID,
            database=DATABASE_ID,
            credentials=credentials
        )
        print("Firestore client initialized.")

    except FileNotFoundError:
        print(f"Error: Service account key not found at {SERVICE_ACCOUNT_FILE}")
        # Puedes decidir salir aquí o intentar con ADC si falla el archivo
        return
    except Exception as e:
        print(f"Error initializing Firebase/Firestore: {e}")
        return

    # 2. Crear instancias de las capas inferiores (pasando dependencias)
    print("Creating repository and service instances...")
    # El repositorio se inicializa y guarda el cliente db_client
    # Asume que FirebaseRepository.__init__ usa la config global o recibe db_client
    firebase_repo = FirebaseRepository()

    # El servicio necesita el repositorio
    poll_service = PollService(repo=firebase_repo)

    # 3. Inicializar la UI de Gradio si se solicitó
    if args.ui: # Verifica si se pasó el argumento --ui
        print("Initializing Gradio UI...")
        # *** CAMBIO CLAVE AQUÍ ***
        # CREA UNA INSTANCIA de la clase GradioUI
        gradio_ui_instance = GradioUI(poll_service=poll_service) # <-- ¡Creamos una instancia y le pasamos el servicio!

        # 4. Lanzar la interfaz usando el método launch de la INSTANCIA
        print("Launching Gradio interface...")
        # *** CAMBIO CLAVE AQUÍ ***
        # Llama al método launch() de la INSTANCIA que acabas de crear
        gradio_ui_instance.launch()

    else:
        # Aquí iría la lógica para la CLI si no se usa --ui
        print("CLI mode selected (not implemented in this example).")
        # from .controllers.cli_controller import CLIController # Importa aquí si solo se usa en CLI
        # cli_controller = CLIController(poll_service=poll_service)
        # cli_controller.run() # O el método que inicie tu CLI


# Asegúrate de que la función main() se ejecute cuando el script se ejecute directamente
if __name__ == "__main__":
    main()
