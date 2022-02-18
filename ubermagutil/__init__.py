"""Utilities used across Ubermag."""
import pkg_resources
import pytest

from .inherit_docs import inherit_docs
from .tools import hysteresis_values

__version__ = pkg_resources.get_distribution(__name__).version


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import ubermagutil as uu
    ...
    >>> # uu.test()

    """
    return pytest.main(['-v', '--pyargs',
                        'ubermagutil', '-l'])  # pragma: no cover
