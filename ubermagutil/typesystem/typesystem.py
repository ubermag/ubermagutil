from .descriptors import Descriptor


def typesystem(**kwargs):
    """Decorator for imposing typesystem on a class.

    A specific descriptor is associated to class attributes in the argument
    list.

    Examples
    --------
    1. Imposing typesystem on a class.

    >>> import ubermagutil.typesystem as ts
    ...
    >>> @ts.typesystem(a=ts.Scalar(const=True),
    ...                b=ts.Typed(expected_type=str))
    ... class DecoratedClass:
    ...     def __init__(self, a, b):
    ...         self.a = a
    ...         self.b = b
    ...
    >>> dc = DecoratedClass(a=30, b='Mihajlo Pupin')
    >>> dc.a
    30
    >>> dc.b
    'Mihajlo Pupin'
    >>> dc.b = 5.1  # invalid set with float
    Traceback (most recent call last):
       ...
    TypeError: ...
    >>> dc.a = 101  # an attempt to change the constant attribute
    Traceback (most recent call last):
       ...
    AttributeError: ...
    >>> dc.b = 'Nikola Tesla'  # valid set
    >>> dc.b
    'Nikola Tesla'

    """
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                setattr(value, 'name', key)
                setattr(cls, key, value)
        return cls

    return decorate
