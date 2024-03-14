"""Define a Thread class to read from a supplied pipe and add to a queue."""

import threading
from queue import Queue
from typing import IO


class QueueThread(threading.Thread):
    """Thread to read from a pipe and add to a queue."""

    def __init__(self, pipe: IO[str], queue: Queue[str]) -> None:
        """Init the class."""
        super().__init__()
        self.pipe = pipe
        self.queue = queue
        self.stop_event = threading.Event()

    def stop(self) -> None:
        """Stop the thread."""
        self.stop_event.set()
        self.join()

    def run(self) -> None:
        """Run the thread."""
        while not self.stop_event.is_set():
            line = self.pipe.readline()
            if line == "":
                break
            self.queue.put(line)
