import joommfutil as ju


def test_version():
    assert isinstance(ju.__version__, str)
    assert '.' in ju.__version__


def test_dependencies():
    assert isinstance(ju.__dependencies__, list)
    assert len(ju.__dependencies__) > 0
