import numbers
import itertools
import collections
import numpy as np


class Descriptor:
    """Base descriptor class from which all descriptors in
    `joommfutil.typesystem` are derived.

    Before setting of the attribute value of the decorated class is
    allowed, certain type and value checks are performed. If type or
    value are not according to the decorator specification,
    `TypeError` or `ValueError` are raised accordingly. If
    `const=True` is passed to the decorator, no value changes to the
    class attribute are allowed after the initial assignment. Deleting
    attributes of a decorated class is not allowed.

    Parameters
    ----------
    name : str
        Decorated class attribute name (the default is None). `name`
        must be a valid Python variable name string. More
        specifically, it must not contain spaces, or start with an
        underscore or a numeric character.
    const : bool, optional
        If `const=True`, the attribute in the decorated class is
        constant and its value cannot be changed after the first set.

    Example
    -------
    1. Deriving a descriptor class from the base class `Descriptor`,
    which only allows positive integer values.

    >>> import joommfutil.typesystem as ts
    ...
    >>> class PositiveInt(ts.Descriptor):
    ...     def __set__(self, instance, value):
    ...        if not isinstance(value, int):
    ...            raise TypeError('Allowed only type(value) == int.')
    ...        if value < 0:
    ...            raise ValueError('Allowed only value >= 0.')
    ...        super().__set__(instance, value)
    ...
    >>> @ts.typesystem(myattribute=PositiveInt)
    ... class DecoratedClass:
    ...     def __init__(self, myattribute):
    ...         self.myattribute = myattribute
    ...
    >>> dc = DecoratedClass(myattribute=5)
    >>> dc.myattribute
    5
    >>> dc.myattribute = 101  # valid set
    >>> dc.myattribute
    101
    >>> dc.myattribute = -1  # invalid set - negative value
    Traceback (most recent call last):
       ...
    ValueError: Allowed only value >= 0.
    >>> dc.myattribute = 3.14  # invalid set - float value
    Traceback (most recent call last):
       ...
    TypeError: Allowed only type(value) == int.
    >>> dc.myattribute  # value has not beed affected by invalid sets
    101

    """
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        """Set method

        If `const=True`, changing the value of a decorated class
        attribute after the initial set is not allowed.

        Raises
        ------
        AttributeError
            If changing the value of a decorated class attribute is
            attempted.

        Example
        -------
        1. Changing the value of a decorated class constant attribute.

        >>> import joommfutil.typesystem as ts
        ...
        >>> @ts.typesystem(myattribute=ts.Descriptor(const=True))
        ... class DecoratedClass:
        ...     def __init__(self, myattribute):
        ...         self.myattribute = myattribute
        ...
        >>> dc = DecoratedClass(myattribute="John Doe")
        >>> dc.myattribute
        'John Doe'
        >>> dc.myattribute = 'Jane Doe'
        Traceback (most recent call last):
           ...
        AttributeError: Changing attribute value is not allowed.

        """
        if hasattr(self, 'const'):
            if not self.const or \
               (self.name not in instance.__dict__ and self.const):
                instance.__dict__[self.name] = value
            else:
                raise AttributeError('Changing attribute value '
                                     'is not allowed.')
        else:
            instance.__dict__[self.name] = value

    def __delete__(self, instance):
        """Delete method

        Deleting the decorated class attribute is never allowed.

        Raises
        ------
        AttributeError
            If deleting decorated class attribute is attempted.

        Example
        -------
        1. Deleting an attribute of a decorated class.

        >>> import joommfutil.typesystem as ts
        ...
        >>> @ts.typesystem(myattribute=ts.Descriptor)
        ... class DecoratedClass:
        ...     def __init__(self, myattribute):
        ...         self.myattribute = myattribute
        ...
        >>> dc = DecoratedClass(myattribute="Nikola Tesla")
        >>> dc.myattribute
        'Nikola Tesla'
        >>> del dc.myattribute
        Traceback (most recent call last):
           ...
        AttributeError: Deleting attribute is not allowed.

        """
        raise AttributeError('Deleting attribute is not allowed.')


class Typed(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Allowed only type(value) = '
                            '{}.'.format(self.expected_type))
        super().__set__(instance, value)


class Scalar(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, numbers.Real):
            raise TypeError('Allowed only type(value) = numbers.Real.')
        if hasattr(self, 'expected_type'):
            if not isinstance(value, self.expected_type):
                raise TypeError('Allowed only type(value) = '
                                '{}.'.format(self.expected_type))
        if hasattr(self, 'unsigned'):
            if self.unsigned and value < 0:
                raise ValueError('Allowed only value >= 0.')
        if hasattr(self, 'positive'):
            if self.positive and value <= 0:
                raise ValueError('Allowed only value > 0.')
        super().__set__(instance, value)


class Vector(Typed):
    expected_type = (list, tuple, np.ndarray)

    def __set__(self, instance, value):
        if not all(isinstance(i, numbers.Real) for i in value):
            raise ValueError('Allowed only type(value[.]) == number.Real')
        if hasattr(self, 'size'):
            if len(value) != self.size:
                raise ValueError('Allowed only len(value) == '
                                 '{}'.format(self.size))
        if hasattr(self, 'unsigned'):
            if self.unsigned and not all(i >= 0 for i in value):
                raise ValueError('Allowed only value[.] >= 0.')
        if hasattr(self, 'positive'):
            if self.positive and not all(i > 0 for i in value):
                raise ValueError('Allowed only value[.] > 0.')
        if hasattr(self, 'component_type'):
            if not all(isinstance(i, self.component_type) for i in value):
                raise ValueError('Allowed only type(value[.]) == '
                                 '{}.'.format(self.component_type))
        super().__set__(instance, value)


class Name(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('Allowed only type(value) = str.')
        if not (value[0].isalpha() or value.startswith('_')):
            raise ValueError('String must start with '
                             'a letter or an underscore.')
        if ' ' in value:
            raise ValueError('String must not contain spaces.')
        super().__set__(instance, value)


class InSet(Descriptor):
    def __set__(self, instance, value):
        if value not in self.allowed_values:
            raise ValueError('Allowed only value from set'
                             '{}.'.format(self.allowed_values))
        super().__set__(instance, value)


class Subset(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, collections.Iterable):
            raise TypeError('value must be an iterable.')
        combs = []
        for i in range(0, len(self.sample_set)+1):
            combs += list(itertools.combinations(self.sample_set, r=i))
        combs = map(set, combs)
        if set(value) not in combs:
            raise ValueError('Allowed only value from set {}.'.format(combs))
        super().__set__(instance, set(value))
