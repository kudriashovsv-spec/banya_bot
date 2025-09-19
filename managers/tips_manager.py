import json
import random
import os

class TipsManager:
    def __init__(self, file_path="data/tips.json"):
        self.file_path = file_path
        self.tips = []
        self.load_tips()

    def load_tips(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.tips = json.load(f)

    def get_random_tip(self):
        if not self.tips:
            return {"text": "Советов пока нет.", "photo": None}
        return random.choice(self.tips)
