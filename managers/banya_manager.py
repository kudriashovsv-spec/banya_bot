class BanyaManager:
    def __init__(self):
        # Простейший пример данных
        self.banias = [
            {"id": 1, "name": "Баня на Кировской"},
            {"id": 2, "name": "Баня у озера"}
        ]

    def get_all_banias(self):
        return self.banias
