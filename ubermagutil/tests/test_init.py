import ubermagutil as uu


def test_version():
    assert isinstance(uu.__version__, str)
    assert '.' in uu.__version__
