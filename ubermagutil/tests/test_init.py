import ubermagutil as uu


def test_version():
    assert isinstance(uu.__version__, str)
    assert '.' in uu.__version__


def test_dependencies():
    assert isinstance(uu.__dependencies__, list)
    assert len(uu.__dependencies__) > 0
