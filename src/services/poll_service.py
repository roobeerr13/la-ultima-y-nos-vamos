# src/services/poll_service.py

from src.repositories.firebase_repo import FirebaseRepository
from typing import Dict, Any, Optional
# No necesitas importar datetime si dejas que Firestore lo maneje

class PollService:
    """
    Business logic for handling polls and potentially user-related data.
    Depends on a repository to interact with data storage.
    """
    def __init__(self, repo: FirebaseRepository):
        """
        Initializes the PollService with a FirebaseRepository instance.

        Args:
            repo: The FirebaseRepository instance to use for data access.
        """
        print("PollService initialized.") # Mensaje de depuración
        self._repo = repo # Almacena la instancia del repositorio

    # ... tus métodos actuales para encuestas ...

    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves all data for a specific user by their UID.

        Args:
            user_id: The Firebase Authentication UID of the user.

        Returns:
            A dictionary with user data, or None if the user document doesn't exist.
        """
        print(f"PollService: Attempting to get data for user ID: {user_id}")
        # Usamos el repositorio para buscar en la colección "users" por el UID
        # Asumimos que tienes una colección llamada "users" en Firestore
        user_data = self._repo.find_by_id("users", user_id)

        if user_data:
            print(f"PollService: Found data for user {user_id}")
        else:
            print(f"PollService: No data found for user {user_id}")

        return user_data

    def get_user_tokens_string(self, user_id: str) -> str:
        """
        Retrieves the tokens for a specific user by their UID and formats as a string.

        Args:
            user_id: The Firebase Authentication UID of the user.

        Returns:
            A string indicating the token count or if the user was not found.
        """
        print(f"PollService: Attempting to get tokens string for user ID: {user_id}")
        user_data = self.get_user_data(user_id) # Reusa el método anterior

        if user_data:
            # Asumiendo que el campo se llama 'app_tokens'
            # Usamos .get() para evitar KeyErrors si el campo 'app_tokens' no existe en el documento
            tokens = user_data.get("app_tokens", "Campo 'app_tokens' no encontrado")
            print(f"PollService: Tokens found: {tokens}")
            return f"Tokens del usuario ({user_id}): {tokens}"
        else:
            return f"Usuario con ID {user_id} no encontrado en la base de datos."

    def get_user_data_json_display(self, user_id: str) -> str:
         """
         Retrieves all data for a specific user and formats as a JSON string for display.

         Args:
             user_id: The Firebase Authentication UID of the user.

         Returns:
             A JSON formatted string with user data, or a message if not found.
         """
         print(f"PollService: Attempting to get user data JSON for ID: {user_id}")
         user_data = self.get_user_data(user_id) # Reusa el método get_user_data

         if user_data:
              import json # Importa json aquí si no lo usas en otro lugar
              # json.dumps convierte el diccionario a una cadena JSON.
              # indent=4 para una salida bonita.
              # default=str maneja tipos no serializables como datetime (los convierte a string)
              try:
                  json_data = json.dumps(user_data, indent=4, default=str)
                  print(f"PollService: Prepared JSON data for {user_id}")
                  return json_data
              except Exception as e:
                  print(f"Error converting user data to JSON for {user_id}: {e}")
                  return f"Error al mostrar los datos del usuario {user_id}."
         else:
              return f"Usuario con ID {user_id} no encontrado en la base de datos."

