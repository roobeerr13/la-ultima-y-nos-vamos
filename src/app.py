import argparse
from .controllers.cli_controller import CLIController
from .ui.gradio_app import create_ui
from .services.poll_service import PollService
from .services.user_service import UserService
from .services.nft_service import NFTService
from .services.chatbot_service import ChatbotService
from .repositories.encuesta_repo import PollRepository
from .repositories.usuario_repo import UserRepository
from .repositories.nft_repo import NFTRepository
from .patterns.strategy import RandomTieBreaker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", action="store_true", help="Launch Gradio UI")
    args = parser.parse_args()

    # Initialize repositories
    poll_repo = PollRepository("polls.json")
    user_repo = UserRepository("users.json")
    nft_repo = NFTRepository("nfts.json")

    # Initialize services
    tie_breaker = RandomTieBreaker()
    poll_service = PollService(poll_repo, tie_breaker)
    user_service = UserService(user_repo)
    nft_service = NFTService(nft_repo)
    chatbot_service = ChatbotService(poll_service)

    # Attach observers
    poll_service.attach(nft_service)  # Mint NFT on vote
    poll_service.attach(chatbot_service)  # Update chatbot on poll events

    if args.ui:
        ui = create_ui(poll_service, chatbot_service, nft_service)
        ui.launch()
    else:
        cli = CLIController(poll_service, user_service, nft_service)
        cli.cmdloop()

if __name__ == "__main__":
    main()