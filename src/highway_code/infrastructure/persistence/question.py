import json
from typing import List

from highway_code.domain.model.question import (
    Question,
    QuestionRepositoryInterface,
    Title,
)


class JsonQuestionRepository(QuestionRepositoryInterface):
    def get_all_question(self, country: str) -> List[Question]:
        with open(f"data/{country}/questions.json", "r", encoding="utf-8") as openfile:
            question_list = []
            questions = json.load(openfile)
            for question in questions:
                question_list.append(
                    Question(
                        question["id"],
                        Title(
                            question["title"]["principal"],
                            question["title"]["sub"] if "sub" in question["title"] else [],
                        ),
                        question["propositions"],
                        question["responses"],
                        question["explication"],
                    )
                )
        return question_list
