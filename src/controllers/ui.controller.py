from typing import List, Dict, Any, Optional
import gradio as gr
from ..services.poll_service import PollService
from ..services.user_service import UserService
from ..services.nft_service import NFTService
from ..services.chatbot_service import ChatbotService
from ..models.encuesta import Poll
from ..ui.gradio_app import create_ui

class UIController:
    def __init__(
        self,
        poll_service: PollService,
        user_service: UserService,
        nft_service: NFTService,
        chatbot_service: ChatbotService
    ):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service
        self.current_user: Optional[str] = None

    def login(self, username: str, password: str) -> str:
        """Handle user login and return session token or error message."""
        try:
            session_token = self.user_service.login(username, password)
            self.current_user = username
            return f"Logged in as {username}"
        except ValueError as e:
            return f"Error: {e}"

    def register(self, username: str, password: str) -> str:
        """Handle user registration and return success or error message."""
        try:
            self.user_service.register(username, password)
            return f"User {username} registered successfully"
        except ValueError as e:
            return f"Error: {e}"

    def get_active_polls(self) -> List[str]:
        """Return list of active poll IDs for dropdown."""
        polls = self.poll_service.get_active_polls()
        return [poll.id for poll in polls]

    def get_poll_options(self, poll_id: str) -> List[str]:
        """Return options for a selected poll."""
        poll = self.poll_service.find_by_id(poll_id)
        return poll.options if poll else []

    def vote(self, poll_id: str, option: str, username: Optional[str]) -> str:
        """Handle voting and return success or error message."""
        if not username or username != self.current_user:
            return "Error: Please log in to vote"
        try:
            self.poll_service.vote(poll_id, username, option)
            return f"Vote for '{option}' registered"
        except ValueError as e:
            return f"Error: {e}"

    def get_user_tokens(self, username: Optional[str]) -> List[Dict[str, Any]]:
        """Return list of user's NFT tokens as a table-friendly format."""
        if not username or username != self.current_user:
            return []
        tokens = self.nft_service.get_user_tokens(username)
        return [
            {
                "Token ID": token.token_id,
                "Poll ID": token.poll_id,
                "Option": token.option,
                "Issued At": token.issued_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for token in tokens
        ]

    def transfer_token(self, token_id: str, new_owner: str, username: Optional[str]) -> str:
        """Handle token transfer and return success or error message."""
        if not username or username != self.current_user:
            return "Error: Please log in to transfer tokens"
        try:
            self.nft_service.transfer_token(token_id, username, new_owner)
            return f"Token {token_id} transferred to {new_owner}"
        except ValueError as e:
            return f"Error: {e}"

    def chatbot_respond(self, message: str, username: Optional[str]) -> str:
        """Handle chatbot interaction and return response."""
        if not username or username != self.current_user:
            return "Error: Please log in to use the chatbot"
        return self.chatbot_service.respond(username, message)

    def launch(self) -> None:
        """Launch the Gradio UI with all components."""
        with gr.Blocks() as demo:
            gr.Markdown("# Stream Voting App")

            # Authentication Section
            with gr.Row():
                username_input = gr.Textbox(label="Username")
                password_input = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("Login")
                register_btn = gr.Button("Register")
                auth_output = gr.Textbox(label="Authentication Status")
            
            login_btn.click(
                fn=self.login,
                inputs=[username_input, password_input],
                outputs=auth_output
            )
            register_btn.click(
                fn=self.register,
                inputs=[username_input, password_input],
                outputs=auth_output
            )

            # Polls Section
            with gr.Tab("Polls"):
                poll_dropdown = gr.Dropdown(label="Select Poll", choices=self.get_active_polls())
                option_radio = gr.Radio(label="Vote", choices=[])
                vote_btn = gr.Button("Submit Vote")
                vote_output = gr.Textbox(label="Result")
                
                # Update options when poll is selected
                poll_dropdown.change(
                    fn=self.get_poll_options,
                    inputs=poll_dropdown,
                    outputs=option_radio
                )
                vote_btn.click(
                    fn=self.vote,
                    inputs=[poll_dropdown, option_radio, gr.State(self.current_user)],
                    outputs=vote_output
                )

            # Chatbot Section
            with gr.Tab("Chatbot"):
                gr.ChatInterface(
                    fn=self.chatbot_respond,
                    additional_inputs=[gr.State(self.current_user)],
                    title="Chat with the Stream Bot"
                )

            # NFTs Section
            with gr.Tab("NFTs"):
                tokens_table = gr.Dataframe(label="Your Tokens", value=self.get_user_tokens(self.current_user))
                transfer_id = gr.Textbox(label="Token ID to Transfer")
                new_owner = gr.Textbox(label="New Owner")
                transfer_btn = gr.Button("Transfer")
                transfer_output = gr.Textbox(label="Result")
                
                transfer_btn.click(
                    fn=self.transfer_token,
                    inputs=[transfer_id, new_owner, gr.State(self.current_user)],
                    outputs=transfer_output
                )
                # Refresh tokens table after transfer
                transfer_btn.click(
                    fn=self.get_user_tokens,
                    inputs=[gr.State(self.current_user)],
                    outputs=tokens_table
                )

        demo.launch()