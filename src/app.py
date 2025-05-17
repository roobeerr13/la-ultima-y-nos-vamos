from .controllers.cli_controller import CLIController
from .controllers.ui_controller import UIController
from .services.poll_service import PollService
from .services.user_service import UserService
from .services.nft_service import NFTService
from .services.chatbot_service import ChatbotService
from .services.dashboard_service import DashboardService
from .repositories.mongodb_repo import MongoDBRepository
from .patterns.strategy import RandomTieBreaker
from .ui.gradio_app import create_ui
import sys
from datetime import datetime

def main():
    repo = MongoDBRepository(connection_string="mongodb://localhost:27017/", database_name="streamapp")
    
    initial_poll = {
        "_id": "initial_poll",
        "question": "¿Qué prefieres?",
        "options": ["Opción 1", "Opción 2"],
        "votes": {},
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "duration_seconds": 3600
    }
    initial_user = {
        "_id": "admin",
        "username": "admin",
        "password_hash": "hashed_password_here",
        "token_ids": []
    }
    initial_nft = {
        "_id": "initial_nft",
        "owner": "admin",
        "poll_id": "initial_poll",
        "option": "Opción 1",
        "issued_at": datetime.now().isoformat()
    }
    repo.save("polls", initial_poll["_id"], initial_poll)
    repo.save("users", initial_user["_id"], initial_user)
    repo.save("nfts", initial_nft["_id"], initial_nft)

    tie_breaker = RandomTieBreaker()
    user_service = UserService(repo)
    nft_service = NFTService(repo)
    poll_service = PollService(repo, tie_breaker, nft_service, user_service)
    chatbot_service = ChatbotService(poll_service)
    dashboard_service = DashboardService(poll_service)
    cli_controller = CLIController(poll_service, user_service, nft_service, chatbot_service)
    ui_controller = UIController(poll_service, user_service, nft_service, chatbot_service, dashboard_service)

    if len(sys.argv) > 1 and sys.argv[1] == "--ui":
        print("Lanzando interfaz de Gradio...")
        ui = create_ui(ui_controller)
        ui.launch(show_error=True, debug=True)
    else:
        cli_controller.cmdloop()

    repo.close()

if __name__ == "__main__":
    main()