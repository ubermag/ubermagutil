import pytest
import numbers
import numpy as np
import ubermagutil.typesystem as ts


@ts.typesystem(a=ts.Typed(expected_type=int),
               b=ts.Typed(expected_type=numbers.Real),
               c=ts.Typed(expected_type=str),
               d=ts.Typed(expected_type=list),
               e=ts.Scalar,
               f=ts.Scalar(expected_type=float),
               g=ts.Scalar(positive=True),
               h=ts.Scalar(unsigned=True),
               i=ts.Scalar(expected_type=int, positive=True),
               j=ts.Scalar(expected_type=numbers.Real, positive=False),
               k=ts.Scalar(expected_type=float, unsigned=True),
               l=ts.Vector,
               m=ts.Vector(size=5),
               n=ts.Vector(unsigned=True),
               o=ts.Vector(positive=True),
               p=ts.Vector(size=1, positive=False),
               r=ts.Vector(component_type=int),
               s=ts.Vector(size=3, component_type=float),
               t=ts.Vector(size=2, positive=True, component_type=int),
               u=ts.Name,
               v=ts.Typed(expected_type=str, const=True),
               w=ts.Scalar(positive=True, const=True),
               x=ts.Vector(positive=True, unsigned=True, const=True),
               y=ts.Vector(size=3, component_type=int, const=True),
               z=ts.Name(const=True),
               a1=ts.Subset(sample_set=set([1, 2, '5']), unpack=False),
               b1=ts.Subset(sample_set=set([-1, 5]), unpack=False, const=True),
               c1=ts.Subset(sample_set='xyz', unpack=True),
               d1=ts.Subset(sample_set='xyz', unpack=True, const=True),
               e1=ts.Parameter(descriptor=ts.Scalar(expected_type=int)),
               f1=ts.Parameter(descriptor=ts.Scalar(positive=True)),
               g1=ts.Parameter(descriptor=ts.Vector(size=3)),
               h1=ts.Parameter(descriptor=ts.Scalar(), const=True),
               i1=ts.Scalar(otherwise=tuple),
               j1=ts.Vector(size=3, otherwise=float),
               k1=ts.Parameter(descriptor=ts.Scalar(), otherwise=tuple),
               l1=ts.Parameter(),
               m1=ts.Dictionary(key_descriptor=ts.Name(),
                                value_descriptor=ts.Scalar()),
               n1=ts.Dictionary(value_descriptor=ts.Scalar()),
               o1=ts.Dictionary(key_descriptor=ts.Name(),
                                value_descriptor=ts.Scalar(),
                                allow_empty=True),
               p1=ts.Dictionary(key_descriptor=ts.Name(),
                                value_descriptor=ts.Scalar(),
                                otherwise=str),
               r1=ts.Dictionary(key_descriptor=ts.Name(),
                                value_descriptor=ts.Scalar(),
                                allow_empty=False))
class DecoratedClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_typed():
    dc = DecoratedClass(a=5, b=-3, c='joommf', d=[-9.1, 6, 7])

    # Valid sets
    dc.a = -999
    dc.b = 3e6
    assert dc.b == 3e6
    dc.c = 'joommf'
    dc.d = []
    assert dc.d == []

    # Invalid sets
    with pytest.raises(TypeError):
        dc.a = 0.1
    with pytest.raises(TypeError):
        dc.b = {}
    with pytest.raises(TypeError):
        dc.c = 5
    with pytest.raises(TypeError):
        dc.d = ()


def test_scalar():
    dc = DecoratedClass(e=1e-2, f=1.1, g=500, h=0, i=1, j=1, k=0.)

    # Valid sets
    dc.e = -1
    dc.f = -5.
    dc.g = 1e-11
    assert dc.h == 0
    dc.h = 101
    assert dc.h == 101
    dc.i = 20
    dc.j = -500
    dc.k = 1.2

    # Invalid sets
    with pytest.raises(TypeError):
        dc.e = []
    with pytest.raises(TypeError):
        dc.f = 5000
    with pytest.raises(ValueError):
        dc.g = 0
    with pytest.raises(ValueError):
        dc.h = -1
    with pytest.raises(TypeError):
        dc.i = 0.1
    with pytest.raises(TypeError):
        dc.j = []
    with pytest.raises(TypeError):
        dc.k = -1  # First caught because it is not float


def test_vector():
    dc = DecoratedClass(l=[1, -2, 1.1],
                        m=(-1, 2.1, 0, 0, 0),
                        n=[0, 5],
                        o=[1e-9, ],
                        p=[5],
                        r=[1, 2, 3], s=[0.1, 0.2, -5.1],
                        t=[100, 200])

    # Valid sets
    dc.l = (1, 5e-9)
    dc.m = np.array([1, 2, 3, 0.1, -1e-9])
    dc.n = [1, 0]
    dc.o = np.array([5, 1e5])
    dc.p = (-5,)
    dc.r = [5, 9]
    assert dc.r == [5, 9]
    dc.s = (11.1, np.pi, 0.0)
    dc.t = [1, 9]

    # Invalid sets
    with pytest.raises(TypeError):
        dc.l = {}
    with pytest.raises(ValueError):
        dc.m = (20, 11)
    with pytest.raises(ValueError):
        dc.n = [-1, 5]
    with pytest.raises(ValueError):
        dc.o = (9, -3)
    with pytest.raises(ValueError):
        dc.p = []
    with pytest.raises(TypeError):
        dc.r = ['a', 1, 3]
    with pytest.raises(TypeError):
        dc.s = [1.1, 2, np.pi]
    with pytest.raises(ValueError):
        dc.t = np.array([])


def test_name():
    dc = DecoratedClass(u='var_name')

    dc.u = 'a1'
    dc.u = 'mesh'
    dc.u = 'a1a'
    dc.u = 'var-name'

    with pytest.raises(TypeError):
        dc.u = 5
    with pytest.raises(ValueError):
        dc.u = '1a'
    with pytest.raises(ValueError):
        dc.u = '-a'
    with pytest.raises(ValueError):
        dc.u = 'val name'


def test_dictionary():
    dc = DecoratedClass(m1={'a': 1, 'b': -3}, o1={}, p1='a')

    dc.m1 = {'a': 15, 'b': -51}  # Valid set
    assert dc.m1 == {'a': 15, 'b': -51}

    dc.o1 = {'a': 15, 'b': -51}  # Valid set
    assert dc.o1 == {'a': 15, 'b': -51}

    with pytest.raises(TypeError):
        dc.m1 = 5

    with pytest.raises(ValueError):
        dc.m1 = {}

    with pytest.raises(ValueError):
        dc.r1 = {}

    with pytest.raises(AttributeError):
        dc.n1 = {'a': 15, 'b': -51}


def test_subset():
    dc = DecoratedClass(a1=1, b1=5, c1='xy', d1=[])

    dc.a1 = '5'  # Valid set

    with pytest.raises(AttributeError):
        dc.b1 = -1  # const == True

    with pytest.raises(ValueError):
        dc.a1 = -1  # Invalid set

    # Valid sets
    dc.c1 = 'x'
    assert dc.c1 == {'x'}
    dc.c1 = []
    dc.c1 = 'yx'
    dc.c1 = 'yxzz'
    with pytest.raises(AttributeError):
        dc.d1 = 'x'  # const == True
    with pytest.raises(ValueError):
        dc.c1 = 'a'  # Invalid set
    with pytest.raises(ValueError):
        dc.c1 = [1]  # Invalid set
    with pytest.raises(TypeError):
        dc.c1 = 1  # Invalid set


def test_const():
    dc = DecoratedClass(v='a', w=3.5, x=(1e9,), y=[1, 2, -5],
                        h1={'r1': 1, 'r2': -3.14})

    # z value has not been set yet
    dc.z = 'var_name'

    # Try to change values of set consts
    with pytest.raises(AttributeError):
        dc.v = 'new_string'
    with pytest.raises(AttributeError):
        dc.w = 1e-9
    with pytest.raises(TypeError):
        dc.x = 0  # Caught earlier than Descriptor __set__ method.
    with pytest.raises(AttributeError):
        dc.y = [1, 2, -5]
    with pytest.raises(AttributeError):
        dc.z = 'new_string'
    with pytest.raises(AttributeError):
        dc.h1 = {'r1': 5, 'r2': -3.14}


def test_add_missing_argument():
    dc = DecoratedClass()
    dc.h = 5
    dc.h = 9.1
    with pytest.raises(ValueError):
        dc.h = -1e-10


def test_del_attribute():
    dc = DecoratedClass(a=5, l=[-1, 1])

    # Attempt deleting attributes
    with pytest.raises(AttributeError):
        del dc.a
    with pytest.raises(AttributeError):
        del dc.j


def test_parameter():
    # Integer scalar allowed
    dc = DecoratedClass(e1=5)
    assert dc.e1 == 5

    dc.e1 = -331
    assert dc.e1 == -331

    dc.e1 = {'mystring': 5}
    assert dc.e1 == {'mystring': 5}

    dc.e1 = {'element1': -1, 'element2': 3112}
    assert dc.e1 == {'element1': -1, 'element2': 3112}

    with pytest.raises(TypeError):
        dc.e1 = -1.2
    with pytest.raises(ValueError):
        dc.e1 = {}
    with pytest.raises(ValueError):
        dc.e1 = {'string with spaces': 1}
    with pytest.raises(TypeError):
        dc.e1 = {'validstring': 1.2}
    with pytest.raises(ValueError):
        dc.e1 = {'validstring': 1, 'invalid string': 2}
    with pytest.raises(TypeError):
        dc.e1 = {'validstring': 1, 'anothervalidstring': 2.1}

    assert dc.e1 == {'element1': -1, 'element2': 3112}

    # Positive scalar allowed
    dc = DecoratedClass(f1=1e-12)
    assert dc.f1 == 1e-12

    dc.f1 = 50e6
    assert dc.f1 == 50e6

    dc.f1 = {'mystring': 50e3}
    assert dc.f1 == {'mystring': 50e3}

    dc.f1 = {'element1': 1, 'element2': 3112.1}
    assert dc.f1 == {'element1': 1, 'element2': 3112.1}

    with pytest.raises(ValueError):
        dc.f1 = -1.2
    with pytest.raises(ValueError):
        dc.f1 = {}
    with pytest.raises(ValueError):
        dc.f1 = {'string with spaces': 1}
    with pytest.raises(TypeError):
        dc.f1 = {'validstring': 'string'}
    with pytest.raises(ValueError):
        dc.f1 = {'validstring': 1, 'invalid string': 2}
    with pytest.raises(ValueError):
        dc.f1 = {'validstring': 1, 'anothervalidstring': -2.1}

    # size 3 vector allowed
    dc = DecoratedClass(g1=(0, 0, 1))
    assert dc.g1 == (0, 0, 1)

    dc.g1 = (1, 2, 1e5)
    assert dc.g1 == (1, 2, 1e5)

    dc.g1 = {'mystring': (1, -1.2, 1e-9)}
    assert dc.g1 == {'mystring': (1, -1.2, 1e-9)}

    dc.g1 = {'element1': (0, 0, 1), 'element2': (0, 0, -1)}
    assert dc.g1 == {'element1': (0, 0, 1), 'element2': (0, 0, -1)}

    with pytest.raises(ValueError):
        dc.g1 = (1, 2)
    with pytest.raises(ValueError):
        dc.g1 = {}
    with pytest.raises(ValueError):
        dc.g1 = {'string with spaces': (0, 0, 1)}
    with pytest.raises(TypeError):
        dc.g1 = {'validstring': 'string'}
    with pytest.raises(ValueError):
        dc.g1 = {'validstring': (0, 0, 1), 'invalid string': (1, 1, 1)}
    with pytest.raises(ValueError):
        dc.g1 = {'validstring': (1, 2, 3), 'anothervalidstring': (1,)}

    # No descriptor argument passed
    with pytest.raises(AttributeError):
        dc = DecoratedClass(l1=(0, 0, 1))


def test_otherwise():
    # Scalar, otherwise tuple
    dc = DecoratedClass(i1=1)
    assert dc.i1 == 1

    dc.i1 = (1, 2, 1e5, 5)
    assert dc.i1 == (1, 2, 1e5, 5)

    with pytest.raises(TypeError):
        dc.g1 = 'string'

    # Size 3 vector, otherwise float
    dc = DecoratedClass(j1=(1, 2, 3))
    assert dc.j1 == (1, 2, 3)

    dc.j1 = 1.2
    assert dc.j1 == 1.2

    with pytest.raises(TypeError):
        dc.j1 = 'string'
    with pytest.raises(TypeError):
        dc.j1 = 5

    # Size 3 vector, otherwise float
    dc = DecoratedClass(k1=(1, 2, 3))
    assert dc.k1 == (1, 2, 3)

    dc.k1 = {'a': 1, 'b': 2}
    assert dc.k1 == {'a': 1, 'b': 2}

    with pytest.raises(TypeError):
        dc.k1 = 'string'
    with pytest.raises(TypeError):
        dc.k1 = {'a': 1, 'b': [1, 2, 3]}
    with pytest.raises(TypeError):
        dc.k1 = [1, 2, 3]
