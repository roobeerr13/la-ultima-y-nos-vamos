import sys
from src.repositories.encuesta_repo import PollRepository
from src.repositories.usuario_repo import UserRepository
from src.repositories.nft_repo import NFTRepository
from src.patterns.strategy import RandomTieBreaker
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.controllers.cli_controller import CLIController
from src.controllers.ui_controller import UIController
from src.ui.gradio_app import create_ui

def main():
    poll_repo = PollRepository()
    user_repo = UserRepository()
    nft_repo = NFTRepository()
    tie_breaker = RandomTieBreaker()
    poll_service = PollService(poll_repo, tie_breaker)
    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    cli_controller = CLIController(poll_service, user_service, nft_service)
    ui_controller = UIController(poll_service, user_service, nft_service)

    if len(sys.argv) > 1 and sys.argv[1] == "--ui":
        print("Launching Gradio UI...")
        ui = create_ui(ui_controller)
        ui.launch(show_error=True, debug=True)
    else:
        cli_controller.cmdloop()