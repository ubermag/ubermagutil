import numbers
import itertools
import numpy as np


class ConstantDescriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = value
        else:
            raise AttributeError("Changing attribute not allowed.")

    def __delete__(self, instance):
        raise AttributeError("Deleting attribute not allowed.")


class ConstantMaxSized(ConstantDescriptor):
    def __init__(self, name=None, **opts):
        if "size" not in opts:
            raise TypeError("Missing size option")
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) != self.size:
            raise TypeError("size must be < " + str(self.size))
        super().__set__(instance, value)


class ConstantTyped(ConstantDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError("Expected " + str(self.expected_type))
        super().__set__(instance, value)


class ConstantFromSet(ConstantDescriptor):
    def __init__(self, name=None, **opts):
        if "allowed_values" not in opts:
            raise TypeError("Missing allowed_values option.")
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if value not in self.allowed_values:
            raise TypeError("Expected value from "
                            "{}.".format(self.allowed_values))
        super().__set__(instance, value)


class ConstantFromCombinations(ConstantDescriptor):
    def __init__(self, name=None, **opts):
        if "sample_set" not in opts:
            raise TypeError("Missing sample_set option.")
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        combs = []
        for i in range(1, len(self.sample_set)+1):
            combs += list(itertools.combinations(self.sample_set, r=i))
        combs = map(set, combs)
        if set(value) not in combs:
            raise TypeError("Expected value from "
                            "{}.".format(combs))
        super().__set__(instance, set(value))

        
class ConstantVector(ConstantTyped):
    expected_type = (list, tuple, np.ndarray)


class ConstantSizedVector(ConstantVector, ConstantMaxSized):
    pass


class ConstantRealVector(ConstantSizedVector):
    def __set__(self, instance, value):
        if not all([isinstance(i, numbers.Real) for i in value]):
            raise TypeError("Expected Real vector components.")
        super().__set__(instance, value)


class ConstantPositiveRealVector(ConstantRealVector):
    def __set__(self, instance, value):
        if not all([i > 0 for i in value]):
            raise TypeError("Expected positive vector components.")
        super().__set__(instance, value)


class ConstantString(ConstantTyped):
    expected_type = str


class ConstantObjectName(ConstantString):
    def __set__(self, instance, value):
        if not (value[0].isalpha() or value[0] == "_"):
            raise TypeError("Object name must start with "
                            "a letter or underscore.")
        if " " in value:
            raise TypeError("Object name must not contain space.")
        super().__set__(instance, value)
