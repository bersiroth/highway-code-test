"""
Test stats logic
"""
from test.command import run_command_with_fixture
from click.testing import CliRunner, Result
from freezegun import freeze_time
from command import cli


def run_stats_command(with_question: bool = False, question_input: str = "b\nn\n", reset: bool = False) -> Result:
    """
    Run stats command with option
    """

    def callback(runner: CliRunner):
        if with_question:
            runner.invoke(cli, ["question"], input=question_input)

    args = []
    if reset:
        args.append("--reset")
    return run_command_with_fixture("stats", args, callback=callback)


def test_stats_command() -> None:
    """
    Test standard stats command (without question)
    """
    # When : I run stats command with input
    result = run_stats_command()
    # Then : Command has no error and I have good stats
    assert result.exit_code == 0
    assert "Session" not in result.output
    assert "Global" in result.output
    assert "Total answer            | 0" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 0" in result.output
    assert "Last answer date        | 1999-01-01" in result.output


@freeze_time("2012-09-20")
def test_stats_command_after_question() -> None:
    """
    Test stats command after question
    """
    # Given : I have correctly answered to a question
    answered_to_a_question = True
    question_input = "b\nn\n"
    # When : I run stats command with input
    result = run_stats_command(answered_to_a_question, question_input)
    # Then : Command has no error and I have good stats
    assert result.exit_code == 0
    assert "Session" not in result.output
    assert "Global" in result.output
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 1" in result.output
    assert "Total wrong answer      | 0" in result.output
    assert "Last answer date        | 2012-09-20" in result.output


@freeze_time("2012-09-20")
def test_stats_command_with_reset_after_question() -> None:
    """
    Test stats command after question with reset option
    """
    # Given : I have correctly answered to a question
    answered_to_a_question = True
    question_input = "b\nn\n"
    # When : I run stats command with input
    result = run_stats_command(answered_to_a_question, question_input)
    # Then : Command has no error and I have good stats
    assert result.exit_code == 0
    assert "Total answer            | 1" in result.output
    assert "Total correct answer    | 1" in result.output
    assert "Total wrong answer      | 0" in result.output
    assert "Last answer date        | 2012-09-20" in result.output
    # When : I run stats command with reset option
    result = run_stats_command()
    # Then : Command has no error and I have good reset stats
    assert result.exit_code == 0
    assert "Total answer            | 1" not in result.output
    assert "Total answer            | 0" in result.output
    assert "Total correct answer    | 0" in result.output
    assert "Total wrong answer      | 0" in result.output
    assert "Last answer date        | 1999-01-01" in result.output
