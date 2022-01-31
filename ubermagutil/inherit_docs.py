import types


def inherit_docs(cls):
    """Copy missing docstrings from parent classes.

    Example
    -------
    1. Copy missing docstrings.

    >>> import ubermagutil
    >>> class A:
    ...     def __init__(self, a):
    ...         self.a  = a
    ...
    ...     def square(self):
    ...         return self.a**2
    ...
    ...     square.__doc__ = 'Docstring.'
    ...
    >>> @ubermagutil.inherit_docs
    ... class B(A):
    ...     def square(self):
    ...         return self.a**2
    ...
    >>> B.square.__doc__
    'Docstring.'

    """
    for k, v in vars(cls).items():
        if isinstance(v, types.FunctionType) and not v.__doc__:
            for parent in cls.__bases__:
                parentv = getattr(parent, k, None)
                if parentv and getattr(parentv, '__doc__', None):
                    v.__doc__ = parentv.__doc__
                    break
        elif isinstance(v, property) and not v.fget.__doc__:
            for parent in cls.__bases__:
                parentv = getattr(parent, k, None)
                if parentv and getattr(parentv.fget, '__doc__', None):
                    newprop = property(fget=v.fget, fset=v.fset, fdel=v.fdel,
                                       doc=parentv.fget.__doc__)
                    setattr(cls, k, newprop)
                    break

    return cls
