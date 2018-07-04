import pytest
import numbers
import numpy as np
import joommfutil.typesystem as ts


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

               u=ts.Name)
class DummyClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_typed():
    dc = DummyClass(a=5, b=-3, c="joommf", d=[-9.1, 6, 7])

    # Valid sets
    dc.a = -999
    dc.b = 3e6    
    dc.c = "joommf"
    dc.d = []

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
    dc = DummyClass(e=1e-2, f=1.1, g=500, h=0, i=1, j=1, k=0.)

    # Valid sets
    dc.e = -1
    dc.f = -5.
    dc.g = 1e-11
    dc.h = 101
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
    dc = DummyClass(l=[1, -2, 1.1], m=(-1, 2.1, 0, 0, 0), n=[0, 5], o=[1e-9,],
                    p=[5], r=[1, 2, 3], s=[0.1, 0.2, -5.1], t=[100, 200])


    # Valid sets
    dc.l = (1, 5e-9)
    dc.m = np.array([1, 2, 3, 0.1, -1e-9])
    dc.n = [1, 0]
    dc.o = np.array([5, 1e5])
    dc.p = (-5,)
    dc.r = [5, 9]
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
        dc.o = (9, -11.0)
    with pytest.raises(ValueError):
        dc.p = []
    with pytest.raises(ValueError):
        dc.r = ["a", 1, 3]
    with pytest.raises(ValueError):
        dc.s = [1.1, 2, np.pi]
    with pytest.raises(ValueError):
        dc.t = np.array([])



def test_name():
    dc = DummyClass(u="var_name")

    dc.u = "a1"
    dc.u = "mesh"
    dc.u = "a1a"
    dc.u = "var-name"

    with pytest.raises(TypeError):
        dc.u = 5
    with pytest.raises(ValueError):
        dc.u = "1a"
    with pytest.raises(ValueError):
        dc.u = "-a"
    with pytest.raises(ValueError):
        dc.u = "val name"






        
def test_add_missing_argument():
    dc = DummyClass()
    dc.h = 5
    dc.h = 9.1
    with pytest.raises(ValueError):
        dc.h = -1e-10

"""
def test_typesystem():
    @ts.typesystem(a=ts.Real,
                   b=ts.Int,
                   c=ts.String,
                   d=ts.UnsignedReal,
                   e=ts.PositiveReal,
                   f=ts.Vector,
                   g=ts.SizedVector(size=2),
                   h=ts.RealVector(size=3),
                   i=ts.PositiveRealVector(size=3),
                   k=ts.ObjectName,
                   l=ts.IntVector(size=3),
                   m=ts.PositiveIntVector(size=3),
                   n=ts.FromSet(allowed_values={1, 2, "b"}),
                   o=ts.FromCombinations(sample_set='xyz'))
    class DummyClass:
        def __init__(self, a, b, c, d, e, f, g, h, i, k, l, m, n, o):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.e = e
            self.f = f
            self.g = g
            self.h = h
            self.i = i
            self.k = k
            self.l = l
            self.m = m
            self.n = n
            self.o = o

    a = 1.7
    b = 2
    c = "abc"
    d = 9.5
    e = 11.
    f = (1, 3, -4, 9)
    g = (1, 2)
    h = (-1, 2, 3.1)
    i = (1, 2, 31.1)
    k = "exchange_energy_name"
    l = (-1, 2, -3)
    m = (1, 2, 3)
    n = 1
    o = set('xy')

    dc = DummyClass(a=a, b=b, c=c, d=d, e=e, f=f, g=g,
                    h=h, i=i, k=k, l=l, m=m, n=n, o=o)

    # Simple assertions
    assert dc.a == a
    assert dc.b == b
    assert dc.c == c
    assert dc.d == d
    assert dc.e == e
    assert dc.f == f
    assert dc.g == g
    assert dc.h == h
    assert dc.i == i
    assert dc.k == k
    assert dc.l == l
    assert dc.m == m
    assert dc.n == n
    assert dc.o == o

    # Valid settings
    dc.a = 77.4
    assert dc.a == 77.4
    dc.b = -77
    assert dc.b == -77
    dc.c = "dummystring"
    assert dc.c == "dummystring"
    dc.d = 61.2
    assert dc.d == 61.2
    dc.e = 0.1
    assert dc.e == 0.1
    dc.f = [1, 2, 3, 4, 5, 6.1]
    assert dc.f == [1, 2, 3, 4, 5, 6.1]
    dc.g = (3, 2.1)
    assert dc.g == (3, 2.1)
    dc.h = (-5, 6, 8)
    assert dc.h == (-5, 6, 8)
    dc.i = (1, 2, 3.2)
    assert dc.i == (1, 2, 3.2)
    dc.k = "_new_name2"
    assert dc.k == "_new_name2"
    dc.l = (-11, -5, 6)
    assert dc.l == (-11, -5, 6)
    dc.m = (5, 9, 879)
    assert dc.m == (5, 9, 879)
    dc.n = "b"
    assert dc.n == "b"
    dc.o = "xzy"
    assert dc.o == set("xyz")

    # Invalid settings
    with pytest.raises(TypeError):
        dc.a = 1+2j
    with pytest.raises(TypeError):
        dc.b = -77.1
    with pytest.raises(TypeError):
        dc.c = 5
    with pytest.raises(TypeError):
        dc.d = -61.2
    with pytest.raises(TypeError):
        dc.e = -0.1
    with pytest.raises(TypeError):
        dc.f = "abc"
    with pytest.raises(TypeError):
        dc.g = (3, 2.1, -6)
    with pytest.raises(TypeError):
        dc.h = (-5, 6, 8, 9)
    with pytest.raises(TypeError):
        dc.h = (-5+1j, 8, 9)
    with pytest.raises(TypeError):
        dc.i = (1, -2, 3.2)
    with pytest.raises(TypeError):
        dc.k = "new name2"
    with pytest.raises(TypeError):
        dc.k = "2newname2"
    with pytest.raises(TypeError):
        dc.l = (1.1, 2, 5)
    with pytest.raises(TypeError):
        dc.m = (0, 2, 5)
    with pytest.raises(TypeError):
        dc.n = -25
    with pytest.raises(TypeError):
        dc.n = "abc"

    # Attempt deleting attribute
    with pytest.raises(AttributeError):
        del dc.i

def test_missing_size_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.SizedVector)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_missing_expected_type_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.TypedAttribute)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_missing_allowed_values_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.FromSet)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_missing_sample_set_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.FromCombinations)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_constanttypesystem():
    @ts.typesystem(a=ts.ConstantRealVector(size=3),
                   b=ts.ConstantPositiveRealVector(size=3),
                   c=ts.ConstantObjectName,
                   d=ts.ConstantFromSet(allowed_values={1, 2, -9}),
                   e=ts.ConstantFromCombinations(sample_set='xyz'))
    class DummyClass:
        def __init__(self, a, b, c, d, e):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.e = e

    a = (0, -1, 2.4)
    b = (1.2, 3.14, 5e-6)
    c = "object_name"
    d = 1
    e = 'xy'

    dc = DummyClass(a=a, b=b, c=c, d=d, e=e)

    # Simple assertions
    assert dc.a == a
    assert dc.b == b
    assert dc.c == c
    assert dc.d == d
    assert dc.e == set(e)

    # Attempt to change value.
    with pytest.raises(AttributeError):
        dc.a = (1, 0, 3)
    with pytest.raises(AttributeError):
        dc.b = (5, 6.1, 7)
    with pytest.raises(AttributeError):
        dc.c = "new_object_name"
    with pytest.raises(AttributeError):
        dc.d = -9
    with pytest.raises(AttributeError):
        dc.e = 'x'

    # Attempt deleting attribute.
    with pytest.raises(AttributeError):
        del dc.a


def test_usecase():
    @ts.typesystem(a=ts.ConstantRealVector(size=3),
                   b=ts.ConstantPositiveRealVector(size=3),
                   c=ts.PositiveReal)
    class DummyClass:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

    a1 = (5, 4, -6.1e-3)
    b1 = (0.1, 2, 3)
    c1 = 9
    dc1 = DummyClass(a=a1, b=b1, c=c1)

    a2 = (1, 1, -2)
    b2 = (9, 10, 12)
    c2 = 78
    dc2 = DummyClass(a=a2, b=b2, c=c2)

    assert dc1.a == a1
    assert dc1.b == b1
    assert dc1.c == c1

    assert dc2.a == a2
    assert dc2.b == b2
    assert dc2.c == c2

    # Attempt to change constant values
    with pytest.raises(AttributeError):
        dc1.a = (1, 0, 3)
    with pytest.raises(AttributeError):
        dc1.b = (5, 6.1, 7)
    with pytest.raises(AttributeError):
        dc2.a = (1, 0, 3)
    with pytest.raises(AttributeError):
        dc2.b = (5, 6.1, 7)

    # Change variable value
    dc1.c = 11

    # Assert values after changes
    assert dc1.a == a1
    assert dc1.b == b1
    assert dc1.c == 11

    assert dc2.a == a2
    assert dc2.b == b2
    assert dc2.c == c2

    # Attempt deleting attributes
    with pytest.raises(AttributeError):
        del dc1.a
    with pytest.raises(AttributeError):
        del dc1.b
    with pytest.raises(AttributeError):
        del dc1.c
    with pytest.raises(AttributeError):
        del dc2.a
    with pytest.raises(AttributeError):
        del dc2.b
    with pytest.raises(AttributeError):
        del dc2.c
"""
