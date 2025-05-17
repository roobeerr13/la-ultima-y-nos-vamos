from pymongo import MongoClient
from typing import Optional, List
from datetime import datetime

class MongoDBRepository:
    def __init__(self, connection_string="mongodb://localhost:27017/", database_name="streamapp"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]

    def save(self, collection: str, doc_id: str, data: dict) -> None:
        if "_id" not in data:
            data["_id"] = doc_id
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        self.db[collection].update_one({"_id": doc_id}, {"$set": data}, upsert=True)

    def find_by_id(self, collection: str, doc_id: str) -> Optional[dict]:
        doc = self.db[collection].find_one({"_id": doc_id})
        if doc:
            if "created_at" in doc and isinstance(doc["created_at"], str):
                doc["created_at"] = datetime.fromisoformat(doc["created_at"])
            return doc
        return None

    def find_by_field(self, collection: str, field: str, value: str) -> Optional[dict]:
        doc = self.db[collection].find_one({field: value})
        if doc:
            if "created_at" in doc and isinstance(doc["created_at"], str):
                doc["created_at"] = datetime.fromisoformat(doc["created_at"])
            return doc
        return None

    def get_all(self, collection: str) -> List[dict]:
        docs = self.db[collection].find()
        result = []
        for doc in docs:
            if "created_at" in doc and isinstance(doc["created_at"], str):
                doc["created_at"] = datetime.fromisoformat(doc["created_at"])
            result.append(doc)
        return result

    def close(self):
        self.client.close()