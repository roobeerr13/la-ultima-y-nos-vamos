import pytest
from unittest.mock import Mock
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.repositories.encuesta_repo import PollRepository
from src.repositories.usuario_repo import UserRepository
from src.repositories.nft_repo import NFTRepository
from src.patterns.strategy import RandomTieBreaker
from uuid import uuid4

@pytest.fixture
def poll_service(tmp_path):
    repo = PollRepository(str(tmp_path / "polls.json"))
    return PollService(repo, RandomTieBreaker())

@pytest.fixture
def user_service(tmp_path):
    repo = UserRepository(str(tmp_path / "users.json"))
    return UserService(repo)

@pytest.fixture
def nft_service(tmp_path):
    repo = NFTRepository(str(tmp_path / "nfts.json"))
    return NFTService(repo)

@pytest.fixture
def chatbot_service(poll_service):
    return ChatbotService(poll_service)

def test_poll_service_create_and_vote(poll_service):
    poll = poll_service.create_poll("Test?", ["A", "B"], 60)
    assert poll.question == "Test?"
    poll_service.vote(poll.id, "user1", "A")
    updated_poll = poll_service.find_by_id(poll.id)
    assert "user1" in updated_poll.votes
    assert updated_poll.votes["user1"] == ["A"]

def test_poll_service_duplicate_vote(poll_service):
    poll = poll_service.create_poll("Test?", ["A", "B"], 60)
    poll_service.vote(poll.id, "user1", "A")
    with pytest.raises(ValueError, match="User already voted"):
        poll_service.vote(poll.id, "user1", "B")

def test_user_service_register_and_login(user_service):
    user_service.register("user1", "password")
    session_token = user_service.login("user1", "password")
    assert isinstance(session_token, str)
    assert len(session_token) == 36  # UUID length

def test_user_service_invalid_login(user_service):
    with pytest.raises(ValueError, match="Invalid credentials"):
        user_service.login("nonexistent", "password")

def test_nft_service_mint_and_transfer(nft_service, poll_service):
    poll = poll_service.create_poll("Test?", ["A", "B"], 60)
    token = nft_service.mint_token("user1", poll.id, "A")
    assert token.owner == "user1"
    nft_service.transfer_token(token.token_id, "user1", "user2")
    updated_token = nft_service.find_by_id(token.token_id)
    assert updated_token.owner == "user2"

def test_nft_service_invalid_transfer(nft_service):
    token = nft_service.mint_token("user1", str(uuid4()), "A")
    with pytest.raises(ValueError, match="Invalid token or owner"):
        nft_service.transfer_token(token.token_id, "user2", "user3")

def test_chatbot_service_poll_query(chatbot_service, poll_service, monkeypatch):
    poll = poll_service.create_poll("Test?", ["A", "B"], 60)
    poll_service.vote(poll.id, "user1", "A")
    # Mock the transformers pipeline
    chatbot_service.chatbot = Mock(return_value=[{"generated_text": "Hi!"}])
    response = chatbot_service.respond("user1", "Who is winning?")
    assert "Current leader: A" in response