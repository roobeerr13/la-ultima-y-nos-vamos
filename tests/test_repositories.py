import pytest
import json
from src.repositories.encuesta_repo import PollRepository
from src.repositories.usuario_repo import UserRepository
from src.repositories.nft_repo import NFTRepository
from src.models.encuesta import Poll
from src.models.usuario import User
from src.models.token_nft import TokenNFT
from uuid import uuid4
from datetime import datetime

@pytest.fixture
def poll_repo(tmp_path):
    return PollRepository(str(tmp_path / "polls.json"))

@pytest.fixture
def user_repo(tmp_path):
    return UserRepository(str(tmp_path / "users.json"))

@pytest.fixture
def nft_repo(tmp_path):
    return NFTRepository(str(tmp_path / "nfts.json"))

def test_poll_repository_save_and_find(poll_repo):
    poll = Poll(
        id=str(uuid4()),
        question="Test?",
        options=["A", "B"],
        votes={},
        status="active",
        created_at=datetime.now(),
        duration_seconds=60
    )
    poll_repo.save(poll)
    retrieved = poll_repo.find_by_id(poll.id)
    assert retrieved.question == poll.question
    assert retrieved.options == poll.options

def test_user_repository_save_and_find(user_repo):
    user = User(
        username="user1",
        password_hash=User.hash_password("password"),
        token_ids=[]
    )
    user_repo.save(user)
    retrieved = user_repo.find_by_username("user1")
    assert retrieved.username == user.username
    assert retrieved.password_hash == user.password_hash

def test_nft_repository_save_and_find(nft_repo):
    token = TokenNFT(
        token_id=TokenNFT.generate_id(),
        owner="user1",
        poll_id=str(uuid4()),
        option="A",
        issued_at=datetime.now()
    )
    nft_repo.save(token)
    retrieved = nft_repo.find_by_id(token.token_id)
    assert retrieved.owner == token.owner
    assert retrieved.option == token.option