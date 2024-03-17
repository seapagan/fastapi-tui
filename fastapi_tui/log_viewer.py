"""Class to provide a Log Viewer widget for the TUI application."""

from __future__ import annotations

import re
from enum import Enum

from textual.widgets import RichLog


class LogLevel(Enum):
    """Enum for log levels.

    These are from memory and need checking!
    """

    DEBUG = "gray"
    INFO = "green"
    WARNING = "yellow"
    ERROR = "red"


class LogViewer(RichLog):
    """A widget to display logs from the server."""

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,  # noqa: A002
        classes: str | None = None,
        disabled: bool = False,  # noqa: FBT001
    ) -> None:
        """Init the class."""
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.highlight = True
        self.markup = True

    def add(
        self,
        line: str,
        no_parse: bool = False,  # noqa: FBT001
    ) -> None:
        """Add a line to the log."""
        if not no_parse:
            log_level, message = self.split_text(line)
            if log_level:
                log_color = LogLevel[log_level.strip()[:-1].upper()].value
                self.write(f"[{log_color}]{log_level}[/{log_color}]{message}")
            else:
                self.write(f"{line}")
        else:
            self.write(line)

    def split_text(self, input_text: str) -> tuple[str | None, str]:
        """Split out the LOG_LEVEL from the message if present.

        Return a tuple of (LOG_LEVEL, message) or (None, message) if no
        LOG_LEVEL string is found.
        """
        pattern = r"^([^:]*:\s+)(.*)|^(.*)$"
        match = re.search(pattern, input_text)

        if match and match.group(1):
            return (match.group(1), match.group(2))
        return None, input_text
