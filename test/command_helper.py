"""
Helper for command
"""
from typing import Callable, List
from click.testing import CliRunner, Result
from command import cli
from fixture.fixture_manager import FixtureManager


def run_command_with_fixture(
    command_name: str, args: List[str], command_input: str = "", callback: Callable = None
) -> Result:
    """
    Run command with fixture
    """
    runner = CliRunner()
    fixture_manager = FixtureManager()
    fixture = fixture_manager.get()
    with runner.isolated_filesystem():
        fixture_manager.load(fixture)
        if callback:
            callback(runner)
        args = [command_name, *args]
        result = runner.invoke(cli, args, input=command_input)
    print(result.output)
    return result
