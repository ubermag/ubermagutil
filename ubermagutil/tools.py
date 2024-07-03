"""Additional tools."""

import contextlib
import os

import numpy as np


def hysteresis_values(vmin, vmax, step):
    """Generate hysteresis values.

    Given ``vmin``, ``vmax``, and ``step``, hysteresis loop values are
    generated and ``list`` is returned. The first and the last values in the
    result are ``vmax``.

    If ``vmax - vmin`` range cannot be divided into integer number of steps,
    ``ValueError`` is raised.

    Parameters
    ----------
    vmin : numbers.Real

        Minimum value

    vmax : numbers.Real

        Maximum value

    step : numbers.Real

        Step value

    Returns
    -------
    list

        Hysteresis values.

    Raises
    ------
    ValueError

        If ``vmax - vmin`` range cannot be divided into integer number of
        steps.

    Examples
    --------
    1. Generate hysteresis values.

    >>> import ubermagutil as uu
    ...
    >>> uu.hysteresis_values(-1, 1, 1)
    [1.0, 0.0, -1.0, 0.0, 1.0]

    """
    rtol = 1e-3
    rem = (vmax - vmin) % step
    if rtol * step < rem < step - rtol * step:
        msg = "Value range cannot be divided into integer number of steps."
        raise ValueError(msg)

    return np.concatenate(
        [np.arange(vmax, vmin, -step), np.arange(vmin, vmax + rtol * step, step)]
    ).tolist()


@contextlib.contextmanager
def changedir(dirname):
    """Context manager for changing directory."""
    cwd = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(cwd)
