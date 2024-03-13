"""Entry point for the main application loop.

You can customize this file to your liking, or indeed empty it entirely and
start from scratch.
Note that if you remove the 'App' class entirely, you will need to remove the
`[tool.poetry.scripts]` section from pyproject.toml as well (if it exist).
"""

from __future__ import annotations

import shutil
import signal
import subprocess
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (
    Button,
    Footer,
    Header,
    Label,
)


class ServerStatus(Widget):
    """Server status widget."""

    server_status: reactive[str] = reactive("Not Running")

    def render(self) -> str:
        """Render the widget."""
        return f"{self.server_status}"


class FastapiTUI(App[None]):
    """Main Textual application class."""

    CSS_PATH = "styles.tcss"
    TITLE = "FastAPI TUI"
    SUB_TITLE = "[WIP] A Textual UI for FastAPI"

    subproc = None

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        yield Horizontal(
            Button("Start Server", id="start", variant="success"),
            Button("Stop Server", id="stop", variant="error", disabled=True),
            id="buttons",
        )
        yield Horizontal(
            Label("Server Status : ", id="statuslabel"),
            ServerStatus(id="status"),
            id="statusline",
        )
        yield ScrollableContainer(id="log")
        yield Footer()

    def on_mount(self) -> None:
        """Mount the application."""
        self.uvicorn_binary = self.get_uvicorn()

        self.stop_button = self.query_one("#stop")
        self.start_button = self.query_one("#start")

        self.status_label = self.query_one("#status")

    def on_unmount(self) -> None:
        """Stop the server if running when we shutdown."""
        self.stop_server()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "start":
            self.start_server()
        elif event.button.id == "stop":
            self.stop_server()

    def get_uvicorn(self) -> str | None:
        """Get uvicorn absolute path.

        We do it this way to avoid injection by changing the PATH.
        It's overkill but an example how to do it safer.
        """
        python_exe = sys.executable
        if python_exe:
            venv_path = Path(python_exe).parent
            return shutil.which("uvicorn", path=venv_path)
        return None

    def start_server(self) -> None:
        """Start the server."""
        if self.uvicorn_binary and not self.subproc:
            # Start the server process
            self.subproc = subprocess.Popen(
                [  # noqa: S603
                    self.uvicorn_binary,
                    "fastapi_tui.server:api",
                    "--reload",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8",
            )
            if self.subproc:
                self.stop_button.disabled = False
                self.start_button.disabled = True
                self.query_one(ServerStatus).server_status = "Running"
                self.query_one(ServerStatus).styles.color = "lightgreen"

    def stop_server(self) -> None:
        """Stop the server."""
        if self.subproc:
            self.subproc.send_signal(signal.SIGINT)
            self.subproc = None
            self.stop_button.disabled = True
            self.start_button.disabled = False
            try:
                # this will fail if called when the app is exiting.
                self.query_one(ServerStatus).server_status = "Not Running"
                self.query_one(ServerStatus).styles.color = "red"
            except NoMatches:
                pass


if __name__ == "__main__":
    app = FastapiTUI()
    app.run()
