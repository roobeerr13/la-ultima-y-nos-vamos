# import firebase_admin # Puedes comentar o mantener si usas otras funciones de Admin SDK
# from firebase_admin import credentials # Puedes comentar o mantener si usas otras funciones de Admin SDK

# Importa el cliente de firestore directamente desde google.cloud
from google.cloud import firestore
import google.auth  # <-- ¡Importa google.auth!

from typing import Optional, List
from datetime import datetime

SERVICE_ACCOUNT_FILE = "src/serviceAccountKey.json"
PROJECT_ID = 'streamapp-19258'
DATABASE_ID = 'streamapp' # Asegúrate de que esto sea 'streamapp'

try:
    credentials, project = google.auth.load_credentials_from_file(SERVICE_ACCOUNT_FILE)
    db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID, credentials=credentials) 
except FileNotFoundError:
    raise FileNotFoundError(f"El archivo {SERVICE_ACCOUNT_FILE} no se encuentra. Descarga el archivo desde la Consola de Firebase (Configuración del proyecto > Cuentas de servicio > Node.js) y colócalo en src/.")
except Exception as e:
     print(f"Error durante la inicialización de Firebase o Firestore: {e}")
     raise

class FirebaseRepository:
    def save(self, collection: str, doc_id: str, data: dict) -> None:
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        db.collection(collection).document(doc_id).set(data)

    def find_by_id(self, collection: str, doc_id: str) -> Optional[dict]:
        doc = db.collection(collection).document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            if "created_at" in data and isinstance(data["created_at"], str):
                data["created_at"] = datetime.fromisoformat(data["created_at"])
            return data
        return None

    def find_by_field(self, collection: str, field: str, value: str) -> Optional[dict]:
        docs = db.collection(collection).where(field, "==", value).limit(1).stream()
        for doc in docs:
            data = doc.to_dict()
            if "created_at" in data and isinstance(data["created_at"], str):
                data["created_at"] = datetime.fromisoformat(data["created_at"])
            return data
        return None

    def get_all(self, collection: str) -> List[dict]:
        docs = db.collection(collection).stream()
        result = []
        for doc in docs:
            data = doc.to_dict()
            if "created_at" in data and isinstance(data["created_at"], str):
                data["created_at"] = datetime.fromisoformat(data["created_at"])
            result.append(data)
        return result
