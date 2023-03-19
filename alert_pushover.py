import requests

class PushoverAlerts:
    def __init__(self, token, user_key):
        self.token = token
        self.user_key = user_key

    def send_message(self, message):
        requests.post("https://api.pushover.net/1/messages.json", data = {
            "token": self.token,
            "user": self.user_key,
            "message": message
            })