from collections import namedtuple
from unittest.mock import patch

import pytest

Terminal = namedtuple("terminal", ["lines", "columns"])


@pytest.fixture(scope="session", autouse=True)
def os_terminal() -> None:
    terminal = Terminal(24, 80)
    os = patch('highway_code.domain.question.render.os').start()
    os.get_terminal_size.return_value = terminal
