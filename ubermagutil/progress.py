import contextlib
import datetime
import glob
import os
import pathlib
import re
import threading
import time

from tqdm.auto import tqdm
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ProgressBar(threading.Thread):
    """Tqdm progress bar thread for simulation progress.

    Parameters
    ----------
    total : int

        Total number of output files written to disk.

    package_name : str

        Name of the external simulation package.

    runner_name : str

        Name of the ubermag-internal runner for the external package.

    glob_name : str

        Name of the output files used for globbing in the output directory (including
        parent directories, base directory is drive-XX).

    """

    INTERVAL = 1

    def __init__(self, total, package_name, runner_name, glob_name):
        super().__init__()
        self.bar = tqdm(
            total=total,
            desc=f"Running {package_name} ({runner_name})",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files written [{elapsed}]",
        )
        self._terminate = False
        self.glob_name = glob_name

    def run(self):
        """Update the progress bar once per second and close when terminating."""
        while not self._terminate:
            self.bar.n = len(glob.glob(f"{self.glob_name}"))
            self.bar.refresh()
            time.sleep(self.INTERVAL)
        self.bar.n = len(glob.glob(f"{self.glob_name}"))
        self.bar.refresh()
        self.bar.close()

    def terminate(self):
        """Stop a running progress bar thread after the current iteration."""
        self._terminate = True
        self.join()


@contextlib.contextmanager
def bar(total, package_name, runner_name, glob_name):
    progress_bar_thread = ProgressBar(total, package_name, runner_name, glob_name)
    now = datetime.datetime.now()
    progress_bar_thread.start()
    tic = time.time()
    try:
        yield
    finally:
        toc = time.time()
        progress_bar_thread.terminate()
        print(
            f"Running {package_name} ({runner_name})[{now:%Y/%m/%d %H:%M}]"
            f" took {toc - tic:0.1f} s"
        )


@contextlib.contextmanager
def summary(package_name, runner_name):
    now = datetime.datetime.now()
    print(
        f"Running {package_name} ({runner_name})[{now:%Y/%m/%d %H:%M}]... ",
        end="",
    )
    tic = time.time()
    try:
        yield
    finally:
        toc = time.time()
        seconds = "({:0.1f} s)".format(toc - tic)
        print(seconds)  # append seconds to the previous print.


def quiet():
    return contextlib.nullcontext()


class HoloviewsDataProvider(FileSystemEventHandler):
    """Event handler to pass magnetisation files to holoviews pipe."""

    def __init__(self, magnetisation_regex, pipe):
        super().__init__()
        self.magnetisation_regex = magnetisation_regex
        self.pipe = pipe
        self.last_file = 0

    def on_modified(self, event):
        """Update buffer for energy plot."""
        pass

    def on_closed(self, event):
        """Add filename of new output files to buffer."""
        if event.is_directory:
            return
        src_path = pathlib.Path(event.src_path)
        if re.findall(self.magnetisation_regex, src_path.name):
            # mumax3 closes and re-opens magnetisation files, presumably like follows:
            # create file -> close -> open + write data -> close
            # only add file to pipe when it contains data
            if os.path.getsize(src_path) > 0:
                # send updates only twice per second; too much data significantly slows
                # the plotting down (to the point where the live update is unusable)
                now = time.time()
                if now - self.last_file > 0.5:
                    self.last_file = now
                    self.pipe.send(src_path.absolute())


@contextlib.contextmanager
def fs_observer(magnetisation_regex, hv_pipe, recursive=False):
    """Watchdog for new files written by a calculator.

    The current directory is monitored.

    Parameters
    ----------
    magnetisation_regex : str
        Regular expression for magnetisation files.
    hv_pipe : holoviews.streams.Pipe
        Pipe to which magnetisation data filenames are sent.
    recursive : bool, default False
        If True, the directory is monitored recursively.
    """
    observer = Observer()

    hv_data = HoloviewsDataProvider(magnetisation_regex, hv_pipe)
    observer.schedule(event_handler=hv_data, path=".", recursive=recursive)

    observer.start()
    try:
        yield
    finally:
        observer.stop()
        observer.join()
