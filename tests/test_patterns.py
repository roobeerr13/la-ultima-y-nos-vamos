import pytest
from unittest.mock import Mock
from src.patterns.observer import Subject, Observer
from src.patterns.factory import SimplePollFactory
from src.patterns.strategy import RandomTieBreaker, AlphabeticalTieBreaker
from uuid import uuid4
from datetime import datetime

def test_observer_pattern():
    subject = Subject()
    observer = Mock(spec=Observer)
    subject.attach(observer)
    subject.notify_observers("poll_id", "vote", {"username": "user1"})
    observer.update.assert_called_once_with("poll_id", "vote", {"username": "user1"})

def test_factory_pattern():
    factory = SimplePollFactory()
    poll = factory.create_poll("Test?", ["A", "B"], 60)
    assert poll.question == "Test?"
    assert poll.options == ["A", "B"]
    assert poll.status == "active"

def test_strategy_random_tiebreaker():
    strategy = RandomTieBreaker()
    options = ["A", "B", "C"]
    result = strategy.resolve(options)
    assert result in options

def test_strategy_alphabetical_tiebreaker():
    strategy = AlphabeticalTieBreaker()
    options = ["C", "A", "B"]
    result = strategy.resolve(options)
    assert result == "A"