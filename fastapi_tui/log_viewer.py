"""Class to provide a Log Viewer widget for the TUI application."""

from textual.widgets import RichLog


class LogViewer(RichLog):
    """A widget to display logs from the server."""

    def add(self, line: str) -> None:
        """Add a line to the log."""
        self.write(line.strip())
