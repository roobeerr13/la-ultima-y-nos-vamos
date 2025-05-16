import pytest
from src.controllers.cli_controller import CLIController
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.repositories.encuesta_repo import PollRepository
from src.repositories.usuario_repo import UserRepository
from src.repositories.nft_repo import NFTRepository
from src.patterns.strategy import RandomTieBreaker

@pytest.fixture
def cli_controller(tmp_path):
    poll_repo = PollRepository(str(tmp_path / "polls.json"))
    user_repo = UserRepository(str(tmp_path / "users.json"))
    nft_repo = NFTRepository(str(tmp_path / "nfts.json"))
    poll_service = PollService(poll_repo, RandomTieBreaker())
    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    return CLIController(poll_service, user_service, nft_service)

def test_cli_create_poll(cli_controller, capsys):
    cli_controller.do_create_poll("Test?|   Test?|A,B|60")
    captured = capsys.readouterr()
    assert "Poll created" in captured.out

def test_cli_vote_invalid_args(cli_controller, capsys):
    cli_controller.do_vote("invalid")
    captured = capsys.readouterr()
    assert "Error" in captured.out

def test_cli_quit(cli_controller):
    assert cli_controller.do_quit("") is True