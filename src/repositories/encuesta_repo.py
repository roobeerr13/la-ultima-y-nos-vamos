# src/repositories/encuesta_repo.py
import json
from typing import List, Optional
from src.models.encuesta import Poll
from src.models.voto import Vote

class EncuestaRepository:
    def __init__(self, file_path: str = "data/polls.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        try:
            with open(self.file_path, "r") as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, "w") as f:
                json.dump({"polls": [], "votes": []}, f)

    def save_poll(self, poll: Poll):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            data["polls"].append(poll.__dict__)
            f.seek(0)
            json.dump(data, f)

    def get_poll(self, poll_id: str) -> Optional[Poll]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
            for p in data["polls"]:
                if p["id"] == poll_id:
                    return Poll(**p)
        return None

    def save_vote(self, vote: Vote):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            data["votes"].append(vote.__dict__)
            f.seek(0)
            json.dump(data, f)