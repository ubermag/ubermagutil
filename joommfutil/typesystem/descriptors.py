import numbers
import itertools
import numpy as np


class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        if hasattr(self, "const"):
            if not self.const or \
               (self.name not in instance.__dict__ and self.const):
                instance.__dict__[self.name] = value
            else:
                raise AttributeError('Changing attribute value '
                                     'is not allowed.')
        else:
            instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError('Deleting attribute is not allowed.')


class Typed(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected: type(value) = '
                            '{}.'.format(self.expected_type))
        super().__set__(instance, value)


class Scalar(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, numbers.Real):
            raise TypeError('Expected: type(value) = numbers.Real.')
        if hasattr(self, "expected_type"):
            if not isinstance(value, self.expected_type):
                raise TypeError('Expected: type(value) = '
                                '{}.'.format(self.expected_type))
        if hasattr(self, "unsigned"):
            if self.unsigned and value < 0:
                raise ValueError('Expected value >= 0.')
        if hasattr(self, "positive"):
            if self.positive and value <= 0:
                raise ValueError('Expected value > 0.')
        super().__set__(instance, value)


class Vector(Typed):
    expected_type = (list, tuple, np.ndarray)

    def __set__(self, instance, value):
        if not all(isinstance(i, numbers.Real) for i in value):
            raise ValueError('Expected typr(value[.]) == number.Real')
        if hasattr(self, "size"):
            if len(value) != self.size:
                raise ValueError('Expected len(value) == '
                                 '{}'.format(self.size))
        if hasattr(self, "unsigned"):
            if self.unsigned and not all(i >= 0 for i in value):
                raise ValueError('Expected value[.] >= 0.')
        if hasattr(self, "positive"):
            if self.positive and not all(i > 0 for i in value):
                raise ValueError('Expected value[.] > 0.')
        if hasattr(self, 'component_type'):
            if not all(isinstance(i, self.component_type) for i in value):
                raise ValueError('Expected type(value[.]) == '
                                 '{}.'.format(self.component_type))
        super().__set__(instance, value)


class Name(Typed):
    expected_type = str

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('Expected: type(value) = str.')
        if not (value[0].isalpha() or value.startswith('_')):
            raise ValueError('String must start with '
                             'a letter or an underscore.')
        if ' ' in value:
            raise ValueError('String must not contain spaces.')
        super().__set__(instance, value)


class InSet(Descriptor):
    def __set__(self, instance, value):
        if value not in self.allowed_values:
            raise ValueError('Expected value from '
                             '{}.'.format(self.allowed_values))
        super().__set__(instance, value)


class Subset(Descriptor):
    def __set__(self, instance, value):
        combs = []
        for i in range(0, len(self.sample_set)+1):
            combs += list(itertools.combinations(self.sample_set, r=i))
        combs = map(set, combs)
        if set(value) not in combs:
            raise ValueError('Expected value from {}.'.format(combs))
        super().__set__(instance, set(value))
