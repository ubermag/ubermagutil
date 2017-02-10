from .variabledescriptors import Descriptor
from .constantdescriptors import ConstantDescriptor


def typesystem(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, (Descriptor, ConstantDescriptor)):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))

        return cls
    return decorate
