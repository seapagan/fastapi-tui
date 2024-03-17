"""Entry point for the main application loop."""

from __future__ import annotations

import locale
import shutil
import signal
import subprocess
import sys
from pathlib import Path
from queue import Queue
from typing import IO, cast

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Label

from fastapi_tui.log_viewer import LogViewer
from fastapi_tui.threads import LogThread, QueueThread


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

    BINDINGS = [  # noqa: RUF012
        Binding("ctrl+q", "exit_app", "Quit", key_display="^Q"),
        Binding("ctrl+t", "toggle_server", "Toggle Server", key_display="^T"),
        Binding("ctrl+l", "clear_log", "Clear Log", key_display="^L"),
    ]

    subproc: subprocess.Popen[str] | None = None

    def __init__(self) -> None:
        """Initialize the application."""
        super().__init__()
        self.uvicorn_binary = self.get_uvicorn()
        self.queue: Queue[str] = Queue()

        locale.setlocale(locale.LC_ALL, "")

    def action_exit_app(self) -> None:
        """Exit the application.

        Called when the user presses 'ctrl+q'.
        """
        self.stop_server()
        self.exit()

    def action_toggle_server(self) -> None:
        """Toggle the server.

        Called when the user presses 'ctrl+t'.
        """
        if self.subproc:
            self.stop_server()
        else:
            self.start_server()

    def action_clear_log(self) -> None:
        """Clear the log.

        Called when the user presses 'ctrl+l'.
        """
        self.log_output.clear()

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        # ------------------------ create the widgets ------------------------ #
        self.start_button = Button(
            "Start Server", id="start", variant="success"
        )
        self.stop_button = Button(
            "Stop Server", id="stop", variant="error", disabled=True
        )
        self.clear_button = Button("Clear Log", id="clear", variant="default")
        self.status_label = ServerStatus(id="status")
        self.log_output = LogViewer(id="log")

        # ------------------------ display the widgets ----------------------- #
        yield Header()
        yield Horizontal(
            self.start_button,
            self.stop_button,
            self.clear_button,
            id="buttons",
        )
        yield Horizontal(
            Label("Server Status : ", id="statuslabel"),
            self.status_label,
            id="statusline",
        )
        yield self.log_output
        yield Footer()

    def on_mount(self) -> None:
        """Mount the application."""

    def on_unmount(self) -> None:
        """Stop the server if running when we shutdown."""
        self.stop_server()

    @on(Button.Pressed, "#start")
    def btn_start(self) -> None:
        """Handle the start button press."""
        self.start_server()

    @on(Button.Pressed, "#stop")
    def btn_stop(self) -> None:
        """Handle the start button press."""
        self.stop_server()

    @on(Button.Pressed, "#clear")
    def btn_clear(self) -> None:
        """Handle the clear button press."""
        self.log_output.clear()

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

                self.queue_thread = QueueThread(
                    cast(IO[str], self.subproc.stdout), self.queue
                )
                self.log_thread = LogThread(self.log_output, self.queue)

                self.queue_thread.start()
                self.log_thread.start()

    def stop_server(self) -> None:
        """Stop the server.

        This is called by button press, but also when the application is
        shutting down (from the `on_unmount` method)
        """
        if self.subproc:
            # stop the uvicorn server
            self.stop_server_process()

            self.stop_button.disabled = True
            self.start_button.disabled = False

            # stop the log and queue threads
            self.log_thread.stop()
            self.queue_thread.stop()

            try:
                # this will raise 'NoMatches' if called when we are exiting.
                self.query_one(ServerStatus).server_status = "Not Running"
                self.query_one(ServerStatus).styles.color = "red"
            except NoMatches:
                pass

    def stop_server_process(self) -> None:
        """Stop the actual server process."""
        if self.subproc:
            self.subproc.send_signal(signal.SIGINT)
            self.subproc.wait()
            self.subproc = None


def app() -> None:
    """Run the application."""
    app = FastapiTUI()
    app.run()


if __name__ == "__main__":
    app()
