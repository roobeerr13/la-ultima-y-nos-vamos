from abc import ABC, abstractmethod
from typing import Any, Dict

class Observer(ABC):
    @abstractmethod
    def update(self, poll_id: str, event: str, data: Dict[str, Any]) -> None:
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify_observers(self, poll_id: str, event: str, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.update(poll_id, event, data)