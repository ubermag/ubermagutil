import pkg_resources as pr

__version__ = pr.get_distribution("joommfutil").version


def test():
    import pytest  # pragma: no cover
    pytest.main(["-v", "--pyargs", "joommfutil"])  # pragma: no cover
