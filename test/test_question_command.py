"""
Test question logic
"""
from test.command_helper import run_command_with_fixture
from click.testing import Result


def run_question_command(input_sequence: str = "a\nn\n", stop_on_failure: bool = False) -> Result:
    """
    Run question command with option
    """
    args = []
    if stop_on_failure:
        args.append("--stop-on-failure")
    return run_command_with_fixture("question", args, input_sequence)


def test_question_command_with_correct_answer() -> None:
    """
    Test standard question command
    """
    # Given : I have valid input
    input_sequence = "b\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    print(result)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "(Question 2) : Les feux de recul d'un véhicule sont de couleur ?" in result.output
    assert "[A] rouge           [B] blanche" in result.output
    assert "Enter your answer with label letter separated by comma. (Ex: A,C): b" in result.output
    assert "Correct !" in result.output
    explication = (
        "Les feux de recul d'un véhicule sont de couleur blanche et vous "
        "indiquent que la voiture a enclenché la marche arrière."
    )
    assert explication in result.output
    assert "New question ? [y/n]: n" in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 1" in result.output
    assert "Total wrong answer      | 0" in result.output


def test_question_command_with_wrong_answer_with_stop_on_failure() -> None:
    """
    Test question command must fail with stop on failure flag
    """
    # Given : I have valid input
    input_sequence = "a\nn\n"
    stop_on_failure = True
    # When : I run question command with input
    result = run_question_command(input_sequence, stop_on_failure)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 1
    assert "Enter your answer with label letter separated by comma. (Ex: A,C): a" in result.output
    assert "Wrong ! The good answer is B." in result.output
    explication = (
        "Les feux de recul d'un véhicule sont de couleur blanche et vous "
        "indiquent que la voiture a enclenché la marche arrière."
    )
    assert explication in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 1" in result.output


def test_question_command_with_wrong_answer() -> None:
    """
    Test standard stats command with wrong answer
    """
    # Given : I have valid input
    input_sequence = "a\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "Enter your answer with label letter separated by comma. (Ex: A,C): a" in result.output
    assert "Wrong ! The good answer is B." in result.output
    explication = (
        "Les feux de recul d'un véhicule sont de couleur blanche et vous "
        "indiquent que la voiture a enclenché la marche arrière."
    )
    assert explication in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 1" in result.output


def test_question_command_with_wrong_label() -> None:
    """
    Question command must validate label
    """
    # Given : I have input with invalid label
    input_sequence = "e\na\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have error message for invalid label
    assert result.exit_code == 0
    assert "ERROR: e is not in labels" in result.output


def test_question_command_with_multiple_question() -> None:
    """
    We can answer to multiple question with only one command
    """
    # Given : I have valid input for two questions
    input_sequence = "b\ny\nb\nn\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "New question ? [y/n]: y" in result.output
    assert "Total answer            | 2" in result.output
    assert "Total correct answer    | 2" in result.output
    assert "Total wrong answer      | 0" in result.output
    assert "Congratulation ! You have answer to all questions" not in result.output


def test_question_command_with_all_questions() -> None:
    """
    We must end question if all questions have been answered
    """
    # Given : I have valid input for two questions
    input_sequence = "b\ny\nb\ny\na\n"
    # When : I run question command with input
    result = run_question_command(input_sequence)
    # Then : Command has no error and I have a good output
    assert result.exit_code == 0
    assert "New question ? [y/n]: y" in result.output
    assert "Total answer            | 3" in result.output
    assert "Total correct answer    | 2" in result.output
    assert "Total wrong answer      | 1" in result.output
    assert "Congratulation ! You have answer to all questions" in result.output
