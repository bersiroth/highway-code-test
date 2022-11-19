from __future__ import annotations

from typing import Callable, List

from click.testing import CliRunner, Result

from fixture.fixture_manager import load_fixture
from highway_code.infrastructure.cli.command import cli


def run_command_with_fixture(
    command_name: str, args: List[str], command_input: str = "", callback: Callable[[CliRunner], None] | None = None
) -> Result:
    runner = CliRunner()
    with runner.isolated_filesystem() as temp_path:
        load_fixture(temp_path)
        if callback:
            callback(runner)
        args = [command_name, *args]
        result = runner.invoke(cli, args, input=command_input, catch_exceptions=False)
    print(result.output)
    return result
