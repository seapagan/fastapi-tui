"""Define a Thread class to read from a queue and log out to the TUI."""

import threading
import time
from queue import Empty, Queue

from fastapi_tui.log_viewer import LogViewer


class LogThread(threading.Thread):
    """A Thread that writes to a RichLog widget."""

    def __init__(self, log_view: LogViewer, queue: Queue[str]) -> None:
        """Init the class."""
        super().__init__()
        self.log_view = log_view
        self.stop_event = threading.Event()
        self.queue = queue

    def stop(self) -> None:
        """Stop the thread."""
        self.stop_event.set()
        self.join()

    def run(self) -> None:
        """Run the thread."""
        while not self.stop_event.is_set():
            try:
                line = self.queue.get_nowait()
            except Empty:  # noqa: PERF203
                time.sleep(0.02)  # lets not grab all the CPU!
            else:
                self.log_view.add(line.strip())

        self.log_view.add("------------")
