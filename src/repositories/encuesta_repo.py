import json
from typing import List, Optional
from src.models.encuesta import Poll
from datetime import datetime  # Added for potential use in Poll deserialization

class PollRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, poll: Poll) -> None:
        data = self._load_data()
        data[poll.id] = poll.__dict__
        self._save_data(data)

    def find_by_id(self, poll_id: str) -> Optional[Poll]:
        data = self._load_data()
        poll_data = data.get(poll_id)
        if poll_data:
            # Convert created_at string back to datetime if needed
            if 'created_at' in poll_data and isinstance(poll_data['created_at'], str):
                poll_data['created_at'] = datetime.fromisoformat(poll_data['created_at'])
            return Poll(**poll_data)
        return None

    def _load_data(self) -> dict:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_data(self, data: dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)  # Ensure datetime is serialized as string