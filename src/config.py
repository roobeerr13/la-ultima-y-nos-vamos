# src/config.py
import yaml

class Config:
    def __init__(self):
        with open("config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        self.db_type = cfg.get("db_type", "json")  # json or sqlite
        self.gradio_port = cfg.get("gradio_port", 7860)
        self.chatbot_model = cfg.get("chatbot_model", "facebook/blenderbot-400M-distill")

CONFIG = Config()