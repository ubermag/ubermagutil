import contextlib
import datetime
import glob
import threading
import time

from tqdm.auto import tqdm


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
            f"Running {package_name} ({runner_name})"
            f"[{now.isoformat(timespec='seconds')}]"
            f" took {toc - tic:0.1f} s"
        )


@contextlib.contextmanager
def summary(package_name, runner_name):
    now = datetime.datetime.now()
    print(
        f"Running {package_name} ({runner_name})"
        f"[{now.isoformat(timespec='seconds')}]... ",
        end="",
    )
    tic = time.time()
    try:
        yield
    finally:
        toc = time.time()
        seconds = f"({toc - tic:0.1f} s)"
        print(seconds)  # append seconds to the previous print.


def quiet():
    return contextlib.nullcontext()
