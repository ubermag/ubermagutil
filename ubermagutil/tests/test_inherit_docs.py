import ubermagutil


def test_inherit_docs():
    class A:
        def __init__(self, a):
            """Docstring 1."""
            self.a = a

        @property
        def square(self):
            """Docstring 2."""
            return self.a**2

        def root(self):
            """Docstring 3."""
            return self.a**0.5

    @ubermagutil.inherit_docs
    class B(A):
        @property
        def square(self):
            return self.a**2

        def root(self):
            return self.a**0.5

    assert A.__init__.__doc__ == 'Docstring 1.'
    assert A.square.__doc__ == 'Docstring 2.'
    assert A.root.__doc__ == 'Docstring 3.'

    assert B.__init__.__doc__ == 'Docstring 1.'
    assert B.square.__doc__ == 'Docstring 2.'
    assert B.root.__doc__ == 'Docstring 3.'
