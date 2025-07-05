# utils/discord_log.py

import logging
import requests

class DiscordWebhookHandler(logging.Handler):
    def __init__(self, webhook_url, level=logging.ERROR):
        super().__init__(level)
        self.webhook_url = webhook_url

    def emit(self, record):
        log_entry = self.format(record)
        try:
            requests.post(self.webhook_url, json={"content": f"[Django Log] {log_entry}"})
        except Exception as e:
            print("Failed to send log to Discord:", e)
