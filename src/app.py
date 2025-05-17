import sys
import os
from src.controllers.cli_controller import CLIController
from src.controllers.ui_controller import UIController
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.services.dashboard_service import DashboardService
from src.repositories.mongodb_repo import MongoDBRepository
from src.patterns.strategy import RandomTieBreaker
from src.ui.gradio_app import create_ui
from datetime import datetime

# Asegurar que src es reconocido como paquete raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    repo = MongoDBRepository(connection_string="mongodb+srv://robertojj2006:n7TW7dDKdWueN4dT@streamapp2.d6ichyj.mongodb.net/", database_name="streamapp")
    
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