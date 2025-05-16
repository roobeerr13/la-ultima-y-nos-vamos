import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.models.usuario import User
from src.models.token_nft import TokenNFT

def test_poll_creation():
    poll = Poll(
        id=str(uuid4()),
        question="Test poll?",
        options=["A", "B"],
        votes={},
        status="active",
        created_at=datetime.now(),
        duration_seconds=60
    )
    assert poll.question == "Test poll?"
    assert poll.options == ["A", "B"]
    assert poll.is_active()

def test_poll_is_active_expired():
    past_time = datetime.now() - timedelta(seconds=61)
    poll = Poll(
        id=str(uuid4()),
        question="Test poll?",
        options=["A", "B"],
        votes={},
        status="active",
        created_at=past_time,
        duration_seconds=60
    )
    assert not poll.is_active()

def test_vote_creation():
    vote = Vote(
        poll_id=str(uuid4()),
        username="user1",
        option="A",
        timestamp=datetime.now()
    )
    assert vote.username == "user1"
    assert vote.option == "A"

def test_user_password_hash():
    password = "password123"
    user = User(
        username="user1",
        password_hash=User.hash_password(password),
        token_ids=[]
    )
    assert user.username == "user1"
    assert len(user.password_hash) > 0
    assert user.password_hash != password  # Ensure it's hashed

def test_token_nft_creation():
    token = TokenNFT(
        token_id=TokenNFT.generate_id(),
        owner="user1",
        poll_id=str(uuid4()),
        option="A",
        issued_at=datetime.now()
    )
    assert token.owner == "user1"
    assert len(token.token_id) == 36  # UUID length