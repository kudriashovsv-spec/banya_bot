class QuizManager:
    def __init__(self):
        self.quiz = [
            {"question": "Сколько раз в неделю рекомендуется посещать баню?",
             "options": ["1 раз", "2-3 раза", "Каждый день"], "answer": 1},
            {"question": "Какая температура в парной оптимальна для новичков?",
             "options": ["40-50°C", "60-70°C", "80-90°C"], "answer": 1},
            {"question": "Что лучше использовать для веников в бане?",
             "options": ["Ивовые", "Березовые", "Хвойные"], "answer": 1}
        ]

    def get_question(self, qid: int):
        return self.quiz[qid] if qid < len(self.quiz) else None
