"""Class to provide a Log Viewer widget for the TUI application."""

from __future__ import annotations

from textual.widgets import RichLog


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

    def add(self, line: str) -> None:
        """Add a line to the log."""
        self.write(line)
