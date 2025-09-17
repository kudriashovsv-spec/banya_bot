class QuizManager:
    def __init__(self):
        self.quiz = [
            {
                "question": "Сколько раз в неделю рекомендуется посещать баню?",
                "options": ["1 раз", "2-3 раза", "Каждый день"],
                "answer": 1  # правильный вариант — "2-3 раза"
            }
        ]

    def get_question(self, qid: int):
        return self.quiz[qid] if qid < len(self.quiz) else None
