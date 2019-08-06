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
               a1=ts.InSet(allowed_values=[1, 2, '5']),
               b1=ts.InSet(allowed_values=[-1, 5], const=True),
               c1=ts.Subset(sample_set='xyz'),
               d1=ts.Subset(sample_set='xyz', const=True))
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
    with pytest.raises(ValueError):
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


def test_inset():
    dc = DecoratedClass(a1=1, b1=5)

    dc.a1 = '5'  # Valid set
    with pytest.raises(AttributeError):
        dc.b1 = -1  # const == True

    with pytest.raises(ValueError):
        dc.a1 = -1  # Invalid set


def test_subset():
    dc = DecoratedClass(c1='xy', d1=[])

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
    dc = DecoratedClass(v='a', w=3.5, x=(1e9,), y=[1, 2, -5])

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
