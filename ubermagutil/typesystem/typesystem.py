from .descriptors import Descriptor


def typesystem(**kwargs):
    """Decorator for imposing typesystem on a decorated class.

    A specific descriptor is associated to class attributes in the
    argument list.

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
    >>> dc = DecoratedClass(a=3.14, b='joommf')
    >>> dc.a
    3.14
    >>> dc.b
    'joommf'
    >>> dc.b = 5  # invalid set with int
    Traceback (most recent call last):
       ...
    TypeError: Allowed only type(value) = <class 'str'>.
    >>> dc.a = 101  # an attempt to change the constant attribute
    Traceback (most recent call last):
       ...
    AttributeError: Changing attribute value is not allowed.
    >>> dc.b = 'Nikola Tesla'
    >>> dc.b
    'Nikola Tesla'

    """
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, (Descriptor)):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate
