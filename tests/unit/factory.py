from typing import List

from highway_code.domain.model.question import Question, Title


def question_factory_test(
    id: int = 1,
    principal_title: str = "Les feux de recul d'un véhicule sont de couleur ?",
    sub_title: List[str] = None,
    propositions: List[str] = None,
    responses: List[str] = None,
    explication: str = "Les feux de recul d'un véhicule sont de couleur blanche.",
) -> Question:
    if sub_title is None:
        sub_title = []
    if propositions is None:
        propositions = ["oui", "non"]
    if responses is None:
        responses = ["oui"]
    return Question(id, Title(principal_title, sub_title), propositions, responses, explication)
