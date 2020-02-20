import pytest
import pkg_resources
from .inherit_docs import inherit_docs

__version__ = pkg_resources.get_distribution(__name__).version
__dependencies__ = pkg_resources.require(__name__)


def test():
    return pytest.main(["-v", "--pyargs", "ubermagutil"])  # pragma: no cover
