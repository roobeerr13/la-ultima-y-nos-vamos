import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional, List
from datetime import datetime

# Inicializa Firebase
cred = credentials.Certificate("src/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class FirebaseRepository:
    def save(self, collection: str, doc_id: str, data: dict) -> None:
        # Convertir datetime a string si es necesario
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        db.collection(collection).document(doc_id).set(data)

    def find_by_id(self, collection: str, doc_id: str) -> Optional[dict]:
        doc = db.collection(collection).document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            # Convertir created_at de string a datetime si existe
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