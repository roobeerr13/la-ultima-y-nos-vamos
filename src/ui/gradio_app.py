import gradio_app as gr
from src.services.poll_service import PollService
from src.services.chatbot_service import ChatbotService
from src.repositories.nft_repo import NFTService

def create_ui(poll_service: PollService, chatbot_service: ChatbotService, nft_service: NFTService):
    with gr.Blocks() as demo:
        gr.Markdown("# Stream Voting App")

        with gr.Tab("Polls"):
            poll_id = gr.Dropdown(label="Select Poll", choices=[p.id for p in poll_service.get_active_polls()])
            option = gr.Radio(label="Vote", choices=[])
            vote_btn = gr.Button("Submit Vote")
            vote_output = gr.Textbox(label="Result")
            vote_btn.click(fn=lambda pid, opt, user: poll_service.vote(pid, user, opt), inputs=[poll_id, option, gr.State("user")], outputs=vote_output)

        with gr.Tab("Chatbot"):
            chatbot = gr.ChatInterface(fn=chatbot_service.respond, additional_inputs=[gr.State("user")])

        with gr.Tab("NFTs"):
            tokens = gr.Dataframe(label="Your Tokens", value=lambda: nft_service.get_user_tokens("user"))
            transfer_id = gr.Textbox(label="Token ID to Transfer")
            new_owner = gr.Textbox(label="New Owner")
            transfer_btn = gr.Button("Transfer")
            transfer_output = gr.Textbox(label="Result")
            transfer_btn.click(fn=lambda tid, no, user: nft_service.transfer_token(tid, user, no), inputs=[transfer_id, new_owner, gr.State("user")], outputs=transfer_output)

    return demo