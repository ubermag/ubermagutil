from .variabledescriptors import Descriptor
from .constantdescriptors import ConstantDescriptor


def typesystem(**kwargs):
    """Decorator for imposing typesystem.

    Examples
    --------
    Simple class decorating.

    >>> import joommfutil.typesystem as ts
    >>> @ts.typesystem(a=ts.UnsignedReal)
    ... class A:
    ...     def __init__(self, a):
    ...         self.a = a
 
    """
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, (Descriptor, ConstantDescriptor)):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))

        return cls
    return decorate
